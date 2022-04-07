import aiohttp
from loguru import logger


async def get_api_response(url, api_key):
    """Async function to get/post requests from/to HTTP or HTTPS"""

    headers = {
        'Crypto-Pay-API-Token': api_key
    }
    async with aiohttp.ClientSession() as session:
        async with session.post(url=url,
                                headers=headers) as response:
            return await response.json()


class CryptoPay:
    def __init__(self, url, api_key):
        self.url = url
        self.api_key = api_key

    async def get_me(self):
        method = 'getMe'
        url = self.url+method
        response = await get_api_response(url, self.api_key)
        print(response)

    async def get_exchange_rate(self, source: str, target: str = 'USD'):
        method = 'getExchangeRates'
        url = self.url+method
        response = await get_api_response(url, self.api_key)

        for exchange in response['result']:
            if exchange['source'] == source and exchange['target'] == target:
                return round(float(1 / float(exchange['rate'])), 3)
        logger.error(f"{source}/{target} - Exchange NOT FOUND")

    async def create_invoice(self, asset: str, amount: float, description: str = None, hidden_message: str = None,
                             paid_btn_name: str = None, paid_btn_url: str = None, payload: str = None,
                             allow_comments: bool = True, allow_anonymous: bool = True, expires_in: int = None) \
            -> dict or None:
        method = 'createInvoice?'

        asset = f'&asset={asset}'
        amount = f'&amount={amount}'
        allow_comments = f'&allow_comments={allow_comments}'
        allow_anonymous = f'&allow_anonymous={allow_anonymous}'

        description = f'&description={description}' if description else ''
        hidden_message = f'&hidden_message={hidden_message}' if hidden_message else ''
        paid_btn_name = f'&paid_btn_name={paid_btn_name}' if paid_btn_name else ''
        paid_btn_url = f'&paid_btn_url={paid_btn_url}' if paid_btn_url else ''
        payload = f'&payload={payload}' if payload else ''
        expires_in = f'&expires_in={expires_in}' if expires_in else ''

        parameters = f'{asset}{amount}{description}{hidden_message}{paid_btn_name}{paid_btn_url}' \
                     f'{payload}{allow_comments}{allow_anonymous}{expires_in}'
        url = self.url+method+parameters
        response = await get_api_response(url, self.api_key)

        logger.debug(f'CREATING INVOICE RESPONSE: {response}')

        if response['ok']:
            return response['result']
        return None

    async def get_paid_invoice(self, invoice_id: str) -> list or None:
        method = 'getInvoices?'
        invoice_id = f'invoice_ids={invoice_id}'
        status = '&status=paid'
        url = self.url+method+invoice_id+status
        response = await get_api_response(url, self.api_key)

        logger.debug(f'PAID INVOICE: {response}')

        if response['result']['items']:
            return response['result']['items']
        else:
            return None






