import json
import logging as log
from dataclasses import dataclass
from datetime import date
from typing import Optional, List

import requests
from dacite import from_dict
from functional import seq

log.basicConfig(level=log.INFO)


@dataclass
class Page:
    uid: str
    title: str

    @classmethod
    def from_pull_result(cls, result: dict):
        return cls(result['block/uid'], result['node/title'])


@dataclass
class Block:
    uid: str
    string: str

    @classmethod
    def from_pull_result(cls, result: dict):
        return Block(result['block/uid'], result['block/string'])

    @classmethod
    def from_create_result(cls, result: dict):
        return Block(result['uid'], result['string'])


class RoamError(RuntimeError):
    object_exists = "cognitect.anomalies/conflict"

    def __init__(self, message, error_type=None):
        super().__init__(message)
        self.type = error_type


def uid_param(uid):
    return [('uid', uid)] if uid else []


class Roam:
    def __init__(self,
                 graph_name: str,
                 key: str,
                 token: str,
                 endpoint: str = 'https://4c67k7zc26.execute-api.us-west-2.amazonaws.com/v1/alphaAPI'):
        self.graph_name = graph_name
        self.key = key
        self.token = token
        self.endpoint = endpoint

    def _send_request(self, action: str, **params):
        payload = dict([('graph-name', self.graph_name)], action=action, **params)
        log.info(f'Sending request to {self.endpoint}. For graph {self.graph_name} \n'
                 f'With payload: {payload}')

        response = requests.post(self.endpoint,
                                 headers={
                                     'x-api-key': self.key,
                                     'x-api-token': self.token,
                                 },
                                 json=payload
                                 )
        log.info(response)
        log.info(response.text)
        self.raise_errors(response)
        result = json.loads(response.text)['success']
        return result

    def query(self, query: str) -> List:
        return seq(self._send_request('q', query=query)).map(lambda it: it[0]).to_list()

    def pull(self, selector, uid):
        return self._send_request('pull', selector=selector, uid=uid)

    def get_page_by_title(self, title: str) -> Page:
        result = self.query(f'[:find (pull ?page [*]) '
                            f':where [?page :node/title "{title}"]'
                            f']')

        return Page.from_pull_result(result[0])

    def get_children(self, uid):
        results = self.query('[:find (pull ?children [*])'
                             ':where '
                             f'[?block :block/uid "{uid}"]'
                             '[?block :block/children ?children]'
                             ']')

        return [Block.from_pull_result(block) for block in results]

    def get_children_by_string(self, parent_uid: str, string: str):
        children = self.get_children(parent_uid)
        return seq(children).filter(lambda it: it.string == string).to_list()

    def get_all_blocks(self):
        return self.query('[ :find (pull ?block [:block/string :block/uid]) :where [?block :block/string]]')

    def create_page(self, title: str, uid: Optional[str] = None):
        result = self._send_request('create-page',
                                    page=dict([('title', title)] + uid_param(uid)))
        return from_dict(Page, result[0])

    @staticmethod
    def raise_errors(response):
        error = json.loads(response.text).get('error')
        if error:
            raise RoamError(error['cognitect.anomalies/message'],
                            error['cognitect.anomalies/category'])

    def create_block(self, parent_uid: str, block: dict, order: int = 0):
        # todo uid support?
        string = next(iter(block))
        response = self._send_request('create-block',
                                      location={'parent-uid': parent_uid, 'order': order},
                                      block={'string': string})

        result = Block.from_create_result(response[0])
        return result, {result.uid: [self.create_block(result.uid, child) for child in reversed(block[string])]}


def strftime(date_format, date_to_format: date):
    def suffix(day):
        return 'th' if 11 <= day <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(day % 10, 'th')

    return date_to_format.strftime(date_format).replace('{S}', str(date_to_format.day) + suffix(date_to_format.day))


def roam_date(date_to_format: date):
    return strftime("%B {S}, %Y", date_to_format)
