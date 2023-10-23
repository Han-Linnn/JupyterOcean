import os
import pickle
import numpy as np
import time
import random
from decimal import Decimal
import requests
# from typing import List
# from ocean_lib.example_config import get_web3
from ocean_lib.ocean.ocean import Ocean
from ocean_lib.example_config import get_config_dict
from ocean_lib.ocean.mint_fake_ocean import mint_fake_OCEAN
# from ocean_lib.web3_internal.wallet import Wallet
from eth_account import Account
# from ocean_lib.web3_internal.constants import ZERO_ADDRESS
# from ocean_lib.common.agreements.service_types import ServiceTypes
from ocean_lib.services.service import Service
# from ocean_lib.data_provider.data_service_provider import DataServiceProvider
# from ocean_lib.web3_internal.currency import pretty_ether_and_wei
from ocean_lib.models.compute_input import ComputeInput
# from ocean_lib.models.btoken import BTokenBase #BToken is ERC20
from ocean_lib.ocean.util import to_wei
from datetime import datetime, timedelta, timezone
from ocean_lib.structures.file_objects import UrlFile
# from ocean_lib.models.datatoken_base import TokenFeeInfo, DatatokenArguments
from ocean_lib.models.fixed_rate_exchange import ExchangeArguments
from ocean_lib.models.datatoken_base import TokenFeeInfo
import pickle

# ================ Remote Setting ====================== #
### use 'get_config_dict()' need to set MUMBAI_RPC_URL env variable.
### 当前Mumbai使用的RPC_URL --> export MUMBAI_RPC_URL=https://polygon-mumbai.infura.io/v3/
### infra账号 --> export WEB3_INFURA_PROJECT_ID='8a76d4cbba2d461697887f12d66e9ddf'
# os.environ['MUMBAI_RPC_URL'] = 'https://polygon-mumbai.infura.io/v3/'
# bob_account = Account.create()
# REMOTE_TEST_PRIVATE_KEY2=bob_account.key.hex()
# os.environ['REMOTE_TEST_PRIVATE_KEY2'] = REMOTE_TEST_PRIVATE_KEY2
# print('Ocean config called !!')
# os.environ['MUMBAI_RPC_URL'] = 'https://rpc-mumbai.maticvigil.com'
os.environ['MUMBAI_RPC_URL'] = 'https://polygon-mumbai.infura.io/v3/' # infura RPC node service provider
# os.environ['WEB3_INFURA_PROJECT_ID'] = '8a76d4cbba2d461697887f12d66e9ddf' # acount 1
os.environ['WEB3_INFURA_PROJECT_ID'] = '7dd18e7dba264b1294e4c0c0206893f1' # account 2 (with Metamask account -- hanlin)
config = get_config_dict("mumbai")
ocean = Ocean(config)
OCEAN = ocean.OCEAN_token
# veOCEAN = ocean.veOCEAN
# network_url = "https://polygon-mumbai.infura.io/v3/8a76d4cbba2d461697887f12d66e9ddf"

# ================ Local Setting (for data farming) ====================== #
# config = get_config_dict("development")
# os.environ['FACTORY_DEPLOYER_PRIVATE_KEY'] = '0xc594c6e5def4bab63ac29eed19a134c130388f74f019bc74b8f4389df2837a58'
# ocean = Ocean(config)
# OCEAN = ocean.OCEAN_token
# mint_fake_OCEAN(config)
# ========================================================================

# ### Rinkeby already deprecte in Infura API. Update on 9.1, Goerli need ETH on Mainnet, abort, use Mumai testnet.
# d = {
#     # 'network' : 'https://rinkeby.infura.io/v3/d163c48816434b0bbb3ac3925d6c6c80',
#     # 'network' : 'https://polygon-mumbai.infura.io/v3/8a76d4cbba2d461697887f12d66e9ddf',
#     'BLOCK_CONFIRMATIONS': 0,
#     # 'RPC_URL': 'https://rpc-mumbai.maticvigil.com',
#     'NETWORK_NAME': 'mumbai',
#     # 'CHAIN_ID': 80001,
#     # 'metadataCacheUri' : 'https://aquarius.oceanprotocol.com',
#     'METADATA_CACHE_URI' : 'https://v4.aquarius.oceanprotocol.com',
#     # 'providerUri' : 'https://provider.rinkeby.oceanprotocol.com',
#     'PROVIDER_URL' : 'https://v4.provider.mumbai.oceanprotocol.com',
#     # 'PROVIDER_ADDRESS': '0x00c6A0BC5cD0078d6Cd0b659E8061B404cfa5704',
#     'web3_instance': get_web3(network_url),
#     'DOWNLOADS_PATH': 'consume-downloads'
# }

# ocean = Ocean(d)
# OCEAN = ocean.OCEAN_token 

class OceanMarket():
    """Ocean Market integration"""
    def __init__(self, private_key=None) -> None:
        # print('OceanMarket class called !')
        self.private_key = private_key
        self.ipfs_account = None
        if private_key is not None:
            self.wallet = Account.from_key(private_key=self.private_key)
        else: 
            self.wallet = None
        # bob_private_key = os.getenv('REMOTE_TEST_PRIVATE_KEY2')
        # self.wallet = Account.from_key(private_key=bob_private_key)
        # self.my_wallet = Account.from_key(private_key='4495afd304f0e4e9a9e0b4a18525a979fa79e2176c518bddcc0ee187adea50bc') # account 1
        # self.my_wallet = Account.from_key(private_key='c0c016dfdd6810ce511c94bd8398372002e4c574d9893f2432c18a53c93b25ef') # new metamask wallet 1 account 1 
        self.my_wallet = Account.from_key(private_key='8527700fe343219722cf25815341dad0eedf3509a425f7fddeacc2eb26dd9a23') # new metamask wallet 1 account 2
        # self.my_wallet = Account.from_key(private_key='d2b713275eaa9d6f2caa5d2db67a6d6caef33460c5ea6eccfe855dad3dd0550a') # new metamask wallet 2 account 1
        self.model = None


    def check_wallet(self) -> None:
        # self.wallet = Wallet(ocean.web3, private_key=self.private_key, transaction_timeout=20, block_confirmations=0)
        # self.wallet = Account.from_key(private_key=self.private_key)
        # self.my_wallet = Account.from_key(private_key='4495afd304f0e4e9a9e0b4a18525a979fa79e2176c518bddcc0ee187adea50bc')
        # print(self.private_key)
        print(f"Vitual Wallet Address = '{self.wallet.address}'")
        print(f"My Wallet Address = '{self.my_wallet.address}'")
        # print(f"Wallet OCEAN = {pretty_ether_and_wei(OCEAN.balanceOf('0xFEeA4195D66A95d44A857216e6fa51F9BE01d657'))}")
        # print(f"Wallet ETH = {pretty_ether_and_wei(ocean.web3.eth.get_balance('0xFEeA4195D66A95d44A857216e6fa51F9BE01d657'))}")
        # Contract合同的oceanAddress设置错了才发不出OCEAN，设置成membai链的ocean contract address 解决。
        # assert OCEAN.balanceOf(self.wallet.address) > 0, "Alice needs OCEAN"
        print(f"My Wallet OCEAN = {OCEAN.balanceOf(self.my_wallet)}")  # 我Metamask钱包里里要有OCEAN才能传给那个随机生成的钱包
        print(f"My Wallet ETH = {ocean.wallet_balance(self.my_wallet)}")

        print(f"Vitual Wallet OCEAN = {OCEAN.balanceOf(self.wallet)}") 
        print(f"Vitual Wallet ETH = {ocean.wallet_balance(self.wallet)}")


    def serach_asset(self, text=None, tag=None):
        if text is None:
            print("Please input the asset name to search!")
            return

        ddos = ocean.assets.query(
            {
                "query": {
                    "query_string": {
                        "query": f"*{text}*",
                        "default_operator": "AND",
                        "fields": ["metadata.name"],
                    }
                }
            }
        )

        # Filter just by the `tags` key
        if tag is not None:
            ddos = list(
                filter(
                    lambda a: tag in a.metadata["tags"],
                    list(filter(lambda a: "tags" in a.metadata.keys(), ddos)),
                )
            )

        count_1 = 0
        for item in ddos:
            count_1 += 1
            print(" ")
            print(f"============================== Asset {count_1} | {item.metadata['type']} | ==============================")
            print(" ")
            print(f"Name -- {item.metadata['name']}")
            print(f"DID  -- {item.did}")
        
            if "tags" in item.metadata:
                print(f"Tags -- {item.metadata['tags']}")

            if "description" in item.metadata:
                print(f"Description -- {item.metadata['description']}")
            
            ## If asset is dataset, show the trusted algo info
            for temp in item.services:
                if temp.type == "compute":
                    # print(temp.compute_values)
                    compute_value = temp.compute_values
                    if compute_value['publisherTrustedAlgorithms']:
                            count_2 = 0
                            for algo in compute_value['publisherTrustedAlgorithms']:
                                count_2 += 1
                                # print(f"algo {count_2} == {algo}")
                                did = algo['did'][7:]
                                trusted_algo_ddos = ocean.assets.query(
                                    {
                                        "query": {
                                            "query_string": {
                                                "query": f"*{did}",
                                                "fields": ["id"],
                                            }
                                        }
                                    }
                                )
                                print(" ")
                                print(f"|| Trusted ALGO {count_2} ||")
                                # print(f"xxxx -- {type(trusted_algo_ddos)}")
                                # print(f"list[0] ==>{trusted_algo_ddos[0]}")
                                print(f"|| -Name- {trusted_algo_ddos[0].metadata['name']}")
                                print(f"|| -DID-  {trusted_algo_ddos[0].did}")
            
            print(" ")
            print("---------------------------------------------------------------------------------")
            print(" ")
        

    ## For search the asset that the current user publish
    def my_profile(self):

        ddos = ocean.assets.query(
            {
                "query": {
                    "query_string": {
                        "query": f"{self.my_wallet.address}",
                        "default_operator": "AND",
                        "fields": ["nft.owner"],
                    }
                }
            }
        )

        count_1 = 0
        for item in ddos:
            count_1 += 1
            print(" ")
            print(f"============================== Asset {count_1} | {item.metadata['type']} | ==============================")
            print(" ")
            print(f"Name -- {item.metadata['name']}")
            print(f"DID  -- {item.did}")
        
            if "tags" in item.metadata:
                print(f"Tags -- {item.metadata['tags']}")

            if "description" in item.metadata:
                print(f"Description -- {item.metadata['description']}")
            
            ## If asset is dataset, show the trusted algo info
            for temp in item.services:
                if temp.type == "compute":
                    # print(temp.compute_values)
                    compute_value = temp.compute_values
                    if compute_value['publisherTrustedAlgorithms']:
                            count_2 = 0
                            for algo in compute_value['publisherTrustedAlgorithms']:
                                count_2 += 1
                                # print(f"algo {count_2} == {algo}")
                                did = algo['did'][7:]
                                trusted_algo_ddos = ocean.assets.query(
                                    {
                                        "query": {
                                            "query_string": {
                                                "query": f"*{did}",
                                                "fields": ["id"],
                                            }
                                        }
                                    }
                                )
                                print(" ")
                                print(f"|| Trusted ALGO {count_2} ||")
                                # print(f"xxxx -- {type(trusted_algo_ddos)}")
                                # print(f"list[0] ==>{trusted_algo_ddos[0]}")
                                print(f"|| -Name- {trusted_algo_ddos[0].metadata['name']}")
                                print(f"|| -DID-  {trusted_algo_ddos[0].did}")
            
            print(" ")
            print("---------------------------------------------------------------------------------")
            print(" ")


    # def check_dt_wallet(self, did):
    #     assert self.wallet is not None, "Ramdom wallet error, initialize app again"
    #     assert self.my_wallet is not None, "Metamask wallet error, please connect Metamask first."
    #     print("Checking the target asset's datatoken...")
    #     asset = ocean.assets.resolve(did)
    #     data_token = ocean.get_datatoken(asset.datatokens[0]["address"])
    #     print(f"I have {data_token.balanceOf(self.my_wallet.address), data_token.symbol()}.")


    # Buy dataset
    def buy_dt_download(self, did):
        # self.wallet = Wallet(ocean.web3, private_key=self.private_key, transaction_timeout=20, block_confirmations=0)
        # self.my_wallet = Wallet(ocean.web3, private_key='4495afd304f0e4e9a9e0b4a18525a979fa79e2176c518bddcc0ee187adea50bc', transaction_timeout=20, block_confirmations=0)
        assert self.wallet is not None, "Random wallet error, initialize app again"
        assert self.my_wallet is not None, "Metamask wallet error, please connect Metamask first."
        ### Get asset DDO instance
        ddo = ocean.assets.resolve(did)
        # print (f"Environment Wallet Address == {asset.datatokens[0]['address']}'")
        # data_token_address = f'0x{did[7:]}'

        #### For buying free asset ####
        # if ddo.stats:
        #     if ddo.stats.get('price'):
        #         price = ddo.stats.get('price')
        #         if price.get('value') == 0:
        #             data_token = ocean.get_datatoken(ddo.datatokens[0]["address"])
        #             data_token.dispense(to_wei(1), {"from": self.my_wallet})
        #             print('Downloading data asset...')
        #             order_tx_id = ocean.assets.pay_for_access_service(ddo, {"from": self.my_wallet}).hex()
        #             asset_dir = ocean.assets.download_asset(ddo, self.my_wallet, './', order_tx_id)
        #             file_name = os.path.join(asset_dir, "test")
        #             print(f"file_name = '{file_name}'")  # e.g. datafile.0xAf07...
        #             return

        ### Buys funds(token) from the asset's pricing schema
        print('Executing Transaction')
        ##  my wallet.
        print(f"Environment Wallet Address = '{self.wallet.address}'")
        print(f"Wallet OCEAN = {OCEAN.balanceOf(self.wallet)}")
        print(f"Wallet ETH = {ocean.wallet_balance(self.wallet)}")
        ### Verify that Bob has ETH
        assert ocean.wallet_balance(self.wallet) > 0, "need test ETH"
        ### Verify that Bob has OCEAN
        assert OCEAN.balanceOf(self.wallet) > 0, "need test OCEAN"
        # print(f"I have {pretty_ether_and_wei(data_token.balanceOf(wallet.address), data_token.symbol())}.")
        # assert data_token.balanceOf(wallet.address) >= to_wei(1), "Bob didn't get 1.0 datatokens"

        ## 从contract中获取datatoken实例.
        data_token = ocean.get_datatoken(ddo.datatokens[0]["address"])
        ##  Get exchange info
        exchange = data_token.get_exchanges()[0]
        # print(f"exchange = '{exchange}'")
        # assert len(exchange) == 1, "The exchange info is empty"

        ##  Bob buys 1.0 datatokens - the amount needed to consume the dataset.
        print(' ')
        print('Buying Dataset Datatoken...')
        provider_fees = ocean.retrieve_provider_fees(
            ddo, ddo.services[0], publisher_wallet=self.wallet
        )
        # else:
        #     provider_fees = ocean.retrieve_provider_fees_for_compute(
        #         ddo, ddo.services[0], publisher_wallet=self.my_wallet
        #     )
        OCEAN.approve(
            data_token.address,
            to_wei(10),
            {"from": self.wallet},
        )

        OCEAN.approve(
            exchange.address,
            to_wei(10),
            {"from": self.wallet},
        )

        tx = data_token.buy_DT_and_order(provider_fees, exchange, {"from": self.wallet}, consumer=self.wallet.address, service_index=0)
        print(f"Already bought datatoken, named {data_token.symbol()}.")

        ## Bob downloads the file. If the connection breaks, Bob can try again
        print('Downloading data asset...')
        asset_dir = ocean.assets.download_asset(ddo, self.wallet, './ocean_download', tx.transactionHash.hex())
        file_name = os.path.join(asset_dir, "file0")
        print(f"File downloaded at '{file_name}'")  # e.g. datafile.0xAf07...
        print('Finished !!')


    # Buy algorithm
    def buy_at_download(self, did):
        # self.wallet = Wallet(ocean.web3, private_key=self.private_key, transaction_timeout=20, block_confirmations=0)
        # self.my_wallet = Wallet(ocean.web3, private_key='4495afd304f0e4e9a9e0b4a18525a979fa79e2176c518bddcc0ee187adea50bc', transaction_timeout=20, block_confirmations=0)
        assert self.wallet is not None, "Random wallet error, initialize app again"
        assert self.my_wallet is not None, "Metamask wallet error, please connect Metamask first."
        ### Get asset DDO instance
        ddo = ocean.assets.resolve(did)
        # print (f"Environment Wallet Address == {asset.datatokens[0]['address']}'")
        # data_token_address = f'0x{did[7:]}'
        
        ### Buys funds(token) from the asset's pricing schema
        print('Executing Transaction')
        ##  wallet
        # print(f"Environment Wallet Address = '{self.my_wallet}'")
        print(f"Wallet OCEAN = {OCEAN.balanceOf(self.wallet)}")
        print(f"Wallet ETH = {ocean.wallet_balance(self.wallet)}")
        ### Verify that Bob has ETH
        assert ocean.wallet_balance(self.wallet) > 0, "Not enough tokens"
        ### Verify that Bob has OCEAN
        assert OCEAN.balanceOf(self.wallet) > 0, "Not enough OCEAN"
        # print(f"I have {pretty_ether_and_wei(data_token.balanceOf(wallet.address), data_token.symbol())}.")
        # assert data_token.balanceOf(wallet.address) >= to_wei(1), "Bob didn't get 1.0 datatokens"

        ## 从contract中获取datatoken实例.
        data_token = ocean.get_datatoken(ddo.datatokens[0]["address"])
        ##  Get exchange info
        exchange = data_token.get_exchanges()[0]
        # print(f"exchange = '{exchange}'")
        # assert len(exchange) == 1, "The exchange info is empty"

        ##  Bob buys 1.0 datatokens - the amount needed to consume the dataset.
        print(' ')
        print('Buying Algorithm Datatoken...')
        ## retrieve_provider_fees只能获取type是‘access’的dataset的provider_fees，不能获取type是‘compute’的
        provider_fees = ocean.retrieve_provider_fees(
            ddo, ddo.services[0], publisher_wallet=self.wallet
        )

        OCEAN.approve(
            data_token.address,
            to_wei(10),
            {"from": self.wallet},
        )

        OCEAN.approve(
            exchange.address,
            to_wei(10),
            {"from": self.wallet},
        )

        tx = data_token.buy_DT_and_order(provider_fees, exchange, {"from": self.wallet}, consumer=self.wallet.address, service_index=0)
        print(f"Already bought datatoken, named {data_token.symbol()}.")

        ## Bob downloads the file. If the connection breaks, Bob can try again
        print('Downloading data asset...')
        asset_dir = ocean.assets.download_asset(ddo, self.wallet, './ocean_download', tx.transactionHash.hex())
        print(asset_dir)
        temp = os.path.join(asset_dir, "file0")
        file_path = os.rename(temp, f"{asset_dir}" + "/" + f"{ddo.metadata.get('name')}" + ".py")
        print(f"File downloaded at '{file_path}'")  # e.g. datafile.0xAf07...
        print('Finished !!')


    # def buy_token_c2d(self, data_token, provider_fees_c2d=None):
    #     # self.wallet = Wallet(ocean.web3, private_key=self.private_key, transaction_timeout=20, block_confirmations=0)
    #     # self.my_wallet = Wallet(ocean.web3, private_key='4495afd304f0e4e9a9e0b4a18525a979fa79e2176c518bddcc0ee187adea50bc', transaction_timeout=20, block_confirmations=0)
    #     assert self.wallet is not None, "Random wallet error, initialize app again"
    #     assert self.my_wallet is not None, "Metamask wallet error, please connect Metamask first."

    #     ### Buys funds(token) from the asset's pricing schema
    #     print('Executing Transaction')

    #     ### Verify that Bob has ETH
    #     assert ocean.wallet_balance(self.my_wallet) > 0, "need test ETH"
    #     ### Verify that Bob has OCEAN
    #     assert OCEAN.balanceOf(self.my_wallet) > 0, "need test OCEAN"

    #     ##  Get exchange info
    #     exchange = data_token.get_exchanges()[0]
    #     # print(f"exchange = '{exchange}'")
    #     # assert len(exchange) == 1, "The exchange info is empty"

    #     ##  Bob buys 1.0 datatokens - the amount needed to consume the dataset.
    #     print('Buying Data Token...')

    #     OCEAN.approve(
    #         data_token.address,
    #         to_wei(10),
    #         {"from": self.my_wallet},
    #     )

    #     OCEAN.approve(
    #         exchange.address,
    #         to_wei(10),
    #         {"from": self.my_wallet},
    #     )

    #     print("token prove End.")
    #     ## 9.14 到这里报错
    #     print(f"{provider_fees_c2d}")
    #     data_token.buy_DT_and_order(
    #         provider_fees = provider_fees_c2d, 
    #         exchange = exchange,
    #         tx_dict = {"from": self.my_wallet}, 
    #         consumer=self.my_wallet.address, 
    #         service_index=0
    #     )
    #     print(f"Already bought {data_token.symbol()}.")


    # def check_exchange(self, dataset_did, algorithm_did):
    #     DATA_ddo = ocean.assets.resolve(dataset_did)  # make sure we operate on the updated and indexed metadata_cache_uri versions
    #     ALGO_ddo = ocean.assets.resolve(algorithm_did)

    #     data_token_address = DATA_ddo.datatokens[0]["address"]
    #     data_token = ocean.get_datatoken(data_token_address)
    #     ALG_address = ALGO_ddo.datatokens[0]["address"]
    #     algo_token = ocean.get_datatoken(ALG_address)

    #     exchange_dt = data_token.get_exchanges()[0]
    #     exchange_at = algo_token.get_exchanges()[0]
        
    #     print(f"data exchange = {exchange_dt}")
    #     print(f"algo exchange = {exchange_at}")


    ### 9.14 测试购买C2D dataset 已通，保持该func不变
    ### 9.14 get_c2d_environments()和get_free_c2d_environment()暂时没区别，就是free env是json，env是个list包含多个env。
    ### Buy datatoken and algo token for C2D
    def _buy_DT_c2d(self, dataset_did, algorithm_did):
        DATA_ddo = ocean.assets.resolve(dataset_did)  # make sure we operate on the updated and indexed metadata_cache_uri versions
        ALGO_ddo = ocean.assets.resolve(algorithm_did)

        data_token_address = DATA_ddo.datatokens[0]["address"]
        data_token = ocean.get_datatoken(data_token_address)
        ALG_address = ALGO_ddo.datatokens[0]["address"]
        algo_token = ocean.get_datatoken(ALG_address)

        ## dataset的ddo的services属性中有‘access’和‘compute’两种的时候,这里要用service_index = 1
        compute_service = DATA_ddo.services[0]
        algo_service = ALGO_ddo.services[0]
        
        c2d_env = ocean.compute.get_free_c2d_environment(compute_service.service_endpoint, DATA_ddo.chain_id)
        print(f"c2d_env::: {c2d_env}")
        print((f"c2d_env ====== ::: {c2d_env['consumerAddress']}"))
        consumerAddress = c2d_env["consumerAddress"]
        computeEnvironment=c2d_env["id"]
        duration = int((datetime.now(timezone.utc) + timedelta(hours=1)).timestamp())

        DATA_compute_input = ComputeInput(DATA_ddo, compute_service)
        ALGO_compute_input = ComputeInput(ALGO_ddo, algo_service)

        print('Retrieving provider fee...')

        provider_fees_c2d = ocean.retrieve_provider_fees_for_compute(
            datasets = [DATA_compute_input], 
            algorithm_data = ALGO_compute_input, 
            consumer_address = consumerAddress, 
            compute_environment = computeEnvironment, 
            valid_until = duration
        )

        print(f"datasets =====> {provider_fees_c2d['datasets'][0]['providerFee']}.")
        print(f"algorithm ====> {provider_fees_c2d['algorithm']['providerFee']}.")
        for i, item in enumerate(provider_fees_c2d["datasets"]):
            print("=======================================")
            print(f"item is ::: {item}")

        print("Executing Transaction...")
        print(" ")
        # normalized_unixtime = time.time() / 1e9
        # amt_send = 1e-8 * (random.random() + normalized_unixtime)
        exchange_dt = data_token.get_exchanges()[0]
        exchange_at = algo_token.get_exchanges()[0]
        ## exchange.buy_DT()

        # print('================')
        # print("token prove End.")
        # print('================')

        ## 报错，checksum_addr(provider_fees["providerFeeAddress"]), ==》 KeyError: 'providerFeeAddress'
        print("Buying dataset datatoken...")
        print('===================')
        OCEAN.approve(
            data_token.address,
            to_wei(10),
            {"from": self.my_wallet},
        )

        OCEAN.approve(
            exchange_dt.address,
            to_wei(10),
            {"from": self.my_wallet},
        )

        tx_dt = data_token.buy_DT_and_order(
            provider_fees = provider_fees_c2d['datasets'][0]['providerFee'], 
            exchange = exchange_dt,
            tx_dict = {"from": self.my_wallet}, 
            consumer=self.my_wallet.address, 
            service_index=0
        )
        tx_dt_id = tx_dt.transactionHash.hex()
        print(f"Already bought datatoken ==> {data_token.symbol()}.")
        print(" ")


        print("Buying algorithm token...")
        print('=========================')
        OCEAN.approve(
            algo_token.address,
            to_wei(10),
            {"from": self.my_wallet},
        )

        OCEAN.approve(
            exchange_at.address,
            to_wei(10),
            {"from": self.my_wallet},
        )
        tx_at = algo_token.buy_DT_and_order(
            provider_fees = provider_fees_c2d['algorithm']['providerFee'], 
            exchange = exchange_at,
            tx_dict = {"from": self.my_wallet}, 
            consumer=self.my_wallet.address, 
            service_index=0
        )
        tx_at_id = tx_at.transactionHash.hex()
        print(f"Already bought algorithm token ==> {algo_token.symbol()}.")
        print(" ")
        ## return the tx_id: Union[str, bytes]
        return tx_dt_id, tx_at_id, c2d_env


    ### C2D接口1！Run Compute-to-data job （只能运行UI上传的asset的c2d，运行ocean.py上传的资产的c2d用c2d_temp()）
    def c2d(self, dataset_did, algorithm_did):
        # algorithm_did = self.algo_publish()
        # dataset_did = self.dt_publish(algorithm_did)

        DATA_ddo = ocean.assets.resolve(dataset_did)  # make sure we operate on the updated and indexed metadata_cache_uri versions
        ALGO_ddo = ocean.assets.resolve(algorithm_did)

        compute_service = DATA_ddo.services[0]
        algo_service = ALGO_ddo.services[0]
        # c2d_env = ocean.compute.get_c2d_environments(compute_service.service_endpoint, DATA_ddo.chain_id)
        # consumerAddress = c2d_env[0]["consumerAddress"]
        # computeEnvironment=c2d_env[0]["id"]
        # duration = int((datetime.now(timezone.utc) + timedelta(days=1)).timestamp())
        
        # print(f"{c2d_env}")
        # print(f"c2d_env--id: {computeEnvironment}")
        # print(f"c2d_env--consumerAddress: {consumerAddress}")
        # print(f"duration: {duration}")

        ## Check if the wallet has DTs and ATs, if not: buy them
        data_token_address = DATA_ddo.datatokens[0]["address"]
        data_token = ocean.get_datatoken(data_token_address)
        ALG_address = ALGO_ddo.datatokens[0]["address"]
        algo_token = ocean.get_datatoken(ALG_address)

        ## Bob need to buy the datatoken and algorithm token first, then he can have token to start order.
        # if data_token.balanceOf(self.my_wallet) < to_wei(1):
        #     print('Not enough datatokens in wallet, buying...')
        #     self.test_buy_dt(data_token)

        # if algo_token.balanceOf(self.my_wallet) < to_wei(1):
        #     print('Not enough algorithm tokens in wallet, buying...')
        #     self.buy_token_c2d(algo_token)
        if data_token.balanceOf(self.my_wallet) < to_wei(1) and algo_token.balanceOf(self.my_wallet) < to_wei(1):
            print('Not enough algorithm & data tokens in wallet, buying...')
            print('=======================================================')
            tx_dt_id, tx_at_id, c2d_env = self._buy_DT_c2d(dataset_did, algorithm_did)

        ## 需要给input的asset两个attributes：transfer_tx_id
        # DATA_compute_input = ComputeInput(DATA_ddo, compute_service, transfer_tx_id = tx_dt)
        # ALGO_compute_input = ComputeInput(ALGO_ddo, algo_service, transfer_tx_id = tx_at)
        datasets = ComputeInput(DATA_ddo, compute_service, transfer_tx_id=tx_dt_id)
        algorithm = ComputeInput(ALGO_ddo, algo_service, transfer_tx_id=tx_at_id)

        ## Pay for dataset and algo for 1 day (有问题，在market上购买data/algo token好像不能用这个来start job)
        # print('Paying for dataset and algo for 1 day...')
        ## 这里的 dataset 和 algo 就是前面 DATA_compute_input 和 ALGO_compute_input 的扩展，多了transfer_tx_id属性
        # datasets, algorithm = ocean.assets.pay_for_compute_service(
        #     datasets=[DATA_compute_input],
        #     algorithm_data=ALGO_compute_input,
        #     consume_market_order_fee_address=self.my_wallet.address,
        #     tx_dict={"from": self.my_wallet},
        #     compute_environment=computeEnvironment,
        #     valid_until=duration,
        #     consumer_address=consumerAddress,
        # )
        # assert datasets, "pay for dataset unsuccessful"
        # assert algorithm, "pay for algorithm unsuccessful"

        ## Start compute job
        print('Starting compute job...')
        job_id = ocean.compute.start(
            consumer_wallet=self.my_wallet,
            dataset=datasets,
            compute_environment=c2d_env["id"],
            algorithm=algorithm,
        )

        print("=====================================================================================")
        print(f"Your job started successfully! Started compute job with id: {job_id}")
        print("=====================================================================================")

        ## Check compute job status
        print('Runing compute job, this might take a while..., check status every 20 sec.')
        succeeded = False
        for i in range(1, 200):
            print(f"--- Checking running status for {i} time ---")
            status = ocean.compute.status(DATA_ddo, compute_service, job_id, self.my_wallet)
            if status.get("dateFinished") and Decimal(status["dateFinished"]) > 0:
                succeeded = True
                break
            print('Still running.')
            print(' ')
            time.sleep(25)
        
        print("=====================")
        print('Done! C2D successful.')
        print("=====================")

        temp = ocean.compute.compute_job_result_logs(DATA_ddo, compute_service, job_id, self.my_wallet)
        if temp:
            result = temp[0]
            print(' ')
            print(f"Compute job log ==> {result}")
            # model = pickle.loads(result)  # the gaussian model result
            # assert len(model) > 0, "unpickle result unsuccessful"
            # self.model = model
        else:
            print(f"Result is empty, compute job finish unsuccessfully.")
    

    ## 测试c2d compute status
    def check_c2d_status(self, dataset_did, job_id):
        DATA_ddo = ocean.assets.resolve(dataset_did)
        compute_service = DATA_ddo.services[0]
        status = ocean.compute.status(DATA_ddo, compute_service, job_id, self.wallet)
        print("=== status info ===")
        print(status)


    ## 查看c2d compute result
    def check_c2d_result(self, dataset_did, job_id):
        DATA_ddo = ocean.assets.resolve(dataset_did)
        compute_service = DATA_ddo.services[0]
        result = ocean.compute.compute_job_result_logs(DATA_ddo, compute_service, job_id, self.wallet)
        print("=== status info ===")
        print(result)


    ###
    #   测试已经购买过的compute job
    #   9.15测试结果：即使在ocean上界面交互形式购买了compute job，pay_for_compute_service()仍然不起作用, 报错‘Not enough datatokens to start Order’
    #   及时换成先exchange.buy_DT也不行，无法进行fix rate exchange, 'execution reverted: FixedRateExchange: This address is not allowed to swap'
    ###
    # def c2d_test(self, dataset_did, algorithm_did):
    #     DATA_ddo = ocean.assets.resolve(dataset_did)  # make sure we operate on the updated and indexed metadata_cache_uri versions
    #     ALGO_ddo = ocean.assets.resolve(algorithm_did)

    #     data_token_address = DATA_ddo.datatokens[0]["address"]
    #     data_token = ocean.get_datatoken(data_token_address)
    #     ALG_address = ALGO_ddo.datatokens[0]["address"]
    #     algo_token = ocean.get_datatoken(ALG_address)

    #     exchange_dt = data_token.get_exchanges()[0]
    #     exchange_at = algo_token.get_exchanges()[0]

    #     OCEAN_needed_dt = exchange_dt.BT_needed(to_wei(1), consume_market_fee=0)
    #     OCEAN.approve(exchange_dt.address, OCEAN_needed_dt, {"from":self.my_wallet})

    #     OCEAN_needed_at = exchange_at.BT_needed(to_wei(1), consume_market_fee=0)
    #     OCEAN.approve(exchange_at.address, OCEAN_needed_at, {"from":self.my_wallet})

    #     print("=============================")
    #     print("keep going")

    #     # D.4 Bob buys datatoken
    #     exchange_dt.buy_DT(to_wei(1), consume_market_fee=0, tx_dict={"from": self.my_wallet})
    #     exchange_at.buy_DT(to_wei(1), consume_market_fee=0, tx_dict={"from": self.my_wallet})

    #     print("=============================")
    #     print("Finished buying needed token.")
    #     print("=============================")

    #     compute_service = DATA_ddo.services[0]
    #     algo_service = ALGO_ddo.services[0]
    #     c2d_env = ocean.compute.get_c2d_environments(compute_service.service_endpoint, DATA_ddo.chain_id)
    #     consumerAddress = c2d_env[0]["consumerAddress"]
    #     computeEnvironment=c2d_env[0]["id"]
    #     duration = int((datetime.now(timezone.utc) + timedelta(days=1)).timestamp())

    #     DATA_compute_input = ComputeInput(DATA_ddo, compute_service)
    #     ALGO_compute_input = ComputeInput(ALGO_ddo, algo_service)

    #     datasets, algorithm = self.pay_for_compute_service(
    #         datasets=[DATA_compute_input],
    #         algorithm_data=ALGO_compute_input,
    #         consume_market_order_fee_address=self.my_wallet.address,
    #         tx_dict={"from": self.my_wallet},
    #         compute_environment=computeEnvironment,
    #         valid_until=duration,
    #         consumer_address=consumerAddress,
    #     )
    #     assert datasets, "pay for dataset unsuccessful"
    #     assert algorithm, "pay for algorithm unsuccessful"
    #     print('========================================================')
    #     print('Paid the compute service! Now you can start compute job.')
    #     print('========================================================')
    #     print(' ')

    #     ## Start compute job
    #     print('Starting compute job...')
    #     job_id = ocean.compute.start(
    #         consumer_wallet=self.my_wallet,
    #         dataset=datasets,
    #         compute_environment=c2d_env[0]["id"],
    #         algorithm=algorithm,
    #     )

    #     print(" ")
    #     print(f"Your job started successfully! Started compute job with id: {job_id}")


    ### publish dataset asset
    def dt_publish(self, DT_name=None, cid=None, algo_did=None):

        # IPFS upload flow
        projectId = "2VYq3ClvhVYDIMihM2w1xIbYWgT"
        projectSecret = "8456ae0837c28f65138b4dcd5415c193"
        endpoint = "https://ipfs.infura.io:5001"
        # IPFS_URI = "https://ipfs.io/ipfs/"

        files = {
            'file': open('./ipfs_files/brain_and_gpr/' + DT_name, 'rb')
        }

        # DT_url = 'https://raw.githubusercontent.com/trentmc/branin/main/branin.arff'
        # DT_name = 'brain.arff'

        ## ADD FILE TO IPFS AND SAVE THE HASH ###
        response1 = requests.post(endpoint + '/api/v0/add', files=files, auth=(projectId, projectSecret))
        print(response1)
        # print(response1.text)
        cid = response1.text.split(",")[1].split(":")[1].replace('"','')
        print(f"cid ==> {cid}")


        DT_url = f"https://han-lin.infura-ipfs.io/ipfs/{cid}"
        if not DT_name:
            now = datetime.now()
            formatted_datetime = now.strftime('%Y-%m-%d-%H:%M')
            DT_name = f"Data-{formatted_datetime}"

        exchange_args = ExchangeArguments(
            rate=to_wei(1), # you can customize this with any price
            base_token_addr=ocean.OCEAN_address, # you can customize this with any ERC20 token
            dt_decimals=18
        )

        print("Publishing data asset on Ocean Market ...")
        print("=========================================")
        (DT_data_nft, DT_datatoken, DT_ddo) = ocean.assets.create_url_asset(
            DT_name, 
            DT_url, 
            {"from": self.my_wallet},
            with_compute=True,
            wait_for_aqua=True, 
            pricing_schema_args=exchange_args
        )
        print(f"DT_data_nft address = '{DT_data_nft.address}'")
        print(f"DT_datatoken address = '{DT_datatoken.address}'")
        if DT_ddo is not None:
            print(" ")
            print("========================================================")
            print("Publish finished! Here is the decentralized identifier(DID):")
            print(DT_ddo.did)
            print("========================================================")
            if algo_did is not None:
                print(" ")
                print("Adding trusted algorithm for dataset...")
                DT_ddo = self.add_trusted_algo(DT_ddo.did, algo_did)
                print("Algorithm is linked to the dataset! You can start C2D.")
                # return DT_ddo.did
        else:
            print("===============================================")
            print("Publish finished! But DDO is not generated yet.")

    ### publish algorithm asset
    def algo_publish(self, file, ALGO_name=None, cid=None, ):
        
        # docker_image = "hln940/ocean_dockers"
        # docker_tag = "latest"
        # docker_checksum = "sha256:037047cda07d1abc2a24c3d3033283cb1983f38fb8379d19445b8b17162b6a96"

        ## IPFS upload flow
        if file is not None and file:
            projectId = "2VYq3ClvhVYDIMihM2w1xIbYWgT"
            projectSecret = "8456ae0837c28f65138b4dcd5415c193"
            endpoint = "https://ipfs.infura.io:5001"
            files = {
                'file': open('./ipfs_files/brain_and_gpr/' + file, 'rb')
            }

            ### ADD FILE TO IPFS AND SAVE THE HASH ###
            print("=====================================")
            print("Uploading algorithm asset on IPFS ...")
            print("=====================================")
            response1 = requests.post(endpoint + '/api/v0/add', files=files, auth=(projectId, projectSecret))
            print(response1)
            # print(response1.text)
            cid = response1.text.split(",")[1].split(":")[1].replace('"','')
            print(f"cid ==> {cid}")
            ALGO_url = f"ipfs.io/ipfs/{cid}"

        # ALGO_url = "https://raw.githubusercontent.com/oceanprotocol/c2d-examples/main/branin_and_gpr/gpr.py"
        if ALGO_name is not None and ALGO_name:
            now = datetime.now()
            formatted_datetime = now.strftime('%Y-%m-%d-%H:%M')
            ALGO_name = f"Algo-{formatted_datetime}"

        exchange_args = ExchangeArguments(
            rate=to_wei(1), # you can customize this with any price
            base_token_addr=ocean.OCEAN_address, # you can customize this with any ERC20 token
            dt_decimals=18
        )

        print("Publishing algorithm asset on Ocean Market ...")
        print("==============================================")
        ## Default publish setting
        (ALGO_data_nft, ALGO_datatoken, ALGO_ddo) = ocean.assets.create_algo_asset(
            ALGO_name, 
            ALGO_url, 
            {"from": self.my_wallet},
            # docker_image,
            # docker_tag,
            # docker_checksum,
            with_compute=True,
            wait_for_aqua=True,
            pricing_schema_args=exchange_args
        )
        print(f"ALGO_data_nft address = '{ALGO_data_nft.address}'")
        print(f"ALGO_datatoken address = '{ALGO_datatoken.address}'")

        if ALGO_ddo is not None:
            print(" ")
            print("============================================================")
            print("Publish finished! Here is the decentralized identifier(DID):")
            print(ALGO_ddo.did)
            print("============================================================")
            # algo_did = ALGO_ddo.did
            # return algo_did
        else:
            print(" ")
            print("===============================================")
            print("Publish finished! But DDO is not generated yet.")

        ## Advance publish setting
        # date_created = "2023-09-28T10:55:11Z"
        # docker_image = "hln940/ocean_dockers"
        # docker_tag = "latest"
        # metadata = {
        #     "created": date_created,
        #     "updated": date_created,
        #     "description": "test Algo",
        #     "name": ALGO_name,
        #     "type": "algorithm",
        #     "author": self.my_wallet.address[:7],
        #     "license": "CC0: PublicDomain",
        #     "algorithm": {
        #         "container": { 
        #             "entrypoint": "python $ALGO", 
        #             "image": docker_image,
        #             "tag": docker_tag, 
        #             "checksum": "sha256:8221d20c1c16491d7d56b9657ea09082c0ee4a8ab1a6621fa720da58b09580e4" 
        #         }, 
        #         "consumerParameters": {} 
        #     } 
        # }
        # (ALGO_data_nft, ALGO_datatoken, ALGO_ddo) = ocean.assets.create(
        #     metadata,
        #     {"from": self.my_wallet}, 
        #     datatoken_args=[DatatokenArguments(files=[ALGO_url])],
        # )
        # print(f"ALGO_data_nft address = '{ALGO_data_nft.address}'")
        # print(f"ALGO_datatoken address = '{ALGO_datatoken.address}'")
        # print(f"ALGO_ddo did = '{ALGO_ddo}'")

        # price = to_wei(10)
        # ALGO_datatoken.create_exchange({"from": self.my_wallet}, price, ocean.OCEAN_address)


    def add_trusted_algo(self, DT_did, ALGO_did):
        DT_ddo = ocean.assets.resolve(DT_did)
        ALGO_ddo = ocean.assets.resolve(ALGO_did)
        compute_service = DT_ddo.services[1]
        compute_service.add_publisher_trusted_algorithm(ALGO_ddo)
        DATA_ddo = ocean.assets.update(DT_ddo, {"from": self.my_wallet})
        print(f"Successfully added trusted algo to dataset ==> '{DATA_ddo}'")
        return DATA_ddo
    

    def publish_and_mint_c2d(self):

        # ocean.py offers multiple file object types. A simple url file is enough for here
        DATA_url_file = UrlFile(
            url="https://raw.githubusercontent.com/oceanprotocol/c2d-examples/main/branin_and_gpr/branin.arff"
        )

        name = "Branin dataset"
        (DATA_data_nft, DATA_datatoken, DATA_ddo) = ocean.assets.create_url_asset(name, DATA_url_file.url, {"from": self.my_wallet}, with_compute=True, wait_for_aqua=True)
        print(f"DATA_data_nft address = '{DATA_data_nft.address}'")
        print(f"DATA_datatoken address = '{DATA_datatoken.address}'")

        print(f"DATA_ddo did = '{DATA_ddo.did}'")

        # Publish data NFT & datatoken for algorithm
        ALGO_url = "https://raw.githubusercontent.com/oceanprotocol/c2d-examples/main/branin_and_gpr/gpr.py"

        name = "grp_from_backend"
        (ALGO_data_nft, ALGO_datatoken, ALGO_ddo) = ocean.assets.create_algo_asset(name, ALGO_url, {"from": self.my_wallet}, wait_for_aqua=True)

        print(f"ALGO_data_nft address = '{ALGO_data_nft.address}'")
        print(f"ALGO_datatoken address = '{ALGO_datatoken.address}'")
        print(f"ALGO_ddo did = '{ALGO_ddo.did}'")

        compute_service = DATA_ddo.services[1]
        compute_service.add_publisher_trusted_algorithm(ALGO_ddo)
        DATA_ddo = ocean.assets.update(DATA_ddo, {"from": self.my_wallet})

        DATA_datatoken.mint(self.wallet, to_wei(5), {"from": self.my_wallet})
        ALGO_datatoken.mint(self.wallet, to_wei(5), {"from": self.my_wallet})

        # Convenience variables
        DATA_did = DATA_ddo.did
        ALGO_did = ALGO_ddo.did

        # Operate on updated and indexed assets
        DATA_ddo = ocean.assets.resolve(DATA_did)
        ALGO_ddo = ocean.assets.resolve(ALGO_did)

        compute_service = DATA_ddo.services[1]
        algo_service = ALGO_ddo.services[0]
        free_c2d_env = ocean.compute.get_free_c2d_environment(compute_service.service_endpoint, DATA_ddo.chain_id)

        DATA_compute_input = ComputeInput(DATA_ddo, compute_service)
        ALGO_compute_input = ComputeInput(ALGO_ddo, algo_service)

        # Pay for dataset and algo for 1 day
        datasets, algorithm = ocean.assets.pay_for_compute_service(
            datasets=[DATA_compute_input],
            algorithm_data=ALGO_compute_input,
            consume_market_order_fee_address=self.wallet.address,
            tx_dict={"from": self.wallet},
            compute_environment=free_c2d_env["id"],
            valid_until=int((datetime.now(timezone.utc) + timedelta(hours=1)).timestamp()),
            consumer_address=free_c2d_env["consumerAddress"],
        )
        assert datasets, "pay for dataset unsuccessful"
        assert algorithm, "pay for algorithm unsuccessful"

        # Start compute job   
        job_id = ocean.compute.start(
            consumer_wallet=self.wallet,
            dataset=datasets[0],
            compute_environment=free_c2d_env["id"],
            algorithm=algorithm,
        )
        print(f"Started compute job with id: {job_id}")

        succeeded = False
        for _ in range(0, 200):
            status = ocean.compute.status(DATA_ddo, compute_service, job_id, self.wallet)
            if status.get("dateFinished") and Decimal(status["dateFinished"]) > 0:
                succeeded = True
                break
            time.sleep(25)
        output = ocean.compute.compute_job_result_logs(
            DATA_ddo, compute_service, job_id, self.wallet
        )
        print(f"output ==> {output}")


    ### C2D接口2！该方法只可以跑ocean.py发布的asset的c2d，UI发布的使用上面c2d() --- 解决方案：不能在pay_for_service前先启动order，会出现serviceID无效
    def temp_c2d(self, dataset_did, algorithm_did):

        DATA_ddo = ocean.assets.resolve(dataset_did)  # make sure we operate on the updated and indexed metadata_cache_uri versions
        ALGO_ddo = ocean.assets.resolve(algorithm_did)

        data_token_address = DATA_ddo.datatokens[0]["address"]
        data_token = ocean.get_datatoken(data_token_address)
        ALG_address = ALGO_ddo.datatokens[0]["address"]
        algo_token = ocean.get_datatoken(ALG_address)

        ## dataset的ddo的services属性中有‘access’和‘compute’两种的时候,这里要用service_index = 1
        compute_service = DATA_ddo.services[1]
        algo_service = ALGO_ddo.services[1]

        # print('Retrieving provider fee...')

        # provider_fees_c2d = ocean.retrieve_provider_fees_for_compute(
        #     datasets = [DATA_compute_input], 
        #     algorithm_data = ALGO_compute_input, 
        #     consumer_address = consumerAddress, 
        #     compute_environment = computeEnvironment, 
        #     valid_until = duration
        # )

        exchange_dt = data_token.get_exchanges()[0]
        exchange_at = algo_token.get_exchanges()[0]
        consume_market_fees = TokenFeeInfo()

        print("Buying datatoken .....")
        print("======================")
        # OCEAN.approve(
        #     data_token.address,
        #     to_wei(10),
        #     {"from": self.my_wallet},
        # )

        OCEAN.approve(
            exchange_dt.address,
            to_wei(10),
            {"from": self.my_wallet},
        )

        exchange_dt.buy_DT(
            datatoken_amt=to_wei(1),
            consume_market_fee_addr=consume_market_fees.address,
            consume_market_fee=consume_market_fees.amount,
            tx_dict={"from": self.my_wallet},
        )
        print(f"Already bought datatoken ==> {data_token.symbol()}.")
        print(" ")

        print("Buying algorithm token .....")
        print("============================")
        # OCEAN.approve(
        #     algo_token.address,
        #     to_wei(10),
        #     {"from": self.my_wallet},
        # )

        OCEAN.approve(
            exchange_at.address,
            to_wei(10),
            {"from": self.my_wallet},
        )

        exchange_at.buy_DT(
            datatoken_amt=to_wei(1),
            consume_market_fee_addr=consume_market_fees.address,
            consume_market_fee=consume_market_fees.amount,
            tx_dict={"from": self.my_wallet},
        )
        print(f"Already bought algorithm token ==> {algo_token.symbol()}.")
        print(" ")

        print("Finished buy DT.")
        print(" ")
        c2d_env = ocean.compute.get_free_c2d_environment(compute_service.service_endpoint, DATA_ddo.chain_id)
        consumerAddress = c2d_env["consumerAddress"]
        computeEnvironment=c2d_env["id"]
        duration = int((datetime.now(timezone.utc) + timedelta(hours=1)).timestamp())

        DATA_compute_input = ComputeInput(DATA_ddo, compute_service)
        ALGO_compute_input = ComputeInput(ALGO_ddo, algo_service)

        # Pay for dataset and algo for 1 day
        print("Paying for compute service ...")
        print("==============================")
        datasets, algorithm = ocean.assets.pay_for_compute_service(
            datasets=[DATA_compute_input],
            algorithm_data=ALGO_compute_input,
            consume_market_order_fee_address=self.my_wallet.address,
            tx_dict={"from": self.my_wallet},
            compute_environment=computeEnvironment,
            valid_until=duration,
            consumer_address=consumerAddress,
        )
        assert datasets, "pay for dataset unsuccessful"
        assert algorithm, "pay for algorithm unsuccessful"
        print(f"This is dataset ==> {datasets}")
        print(f"This is algo ==>{algorithm}")

        # Start compute job
        print(" ")
        print("Starting the compute job ...")
        print("============================")
        job_id = ocean.compute.start(
            consumer_wallet=self.my_wallet,
            dataset=datasets[0],
            compute_environment=computeEnvironment,
            algorithm=algorithm,
        )
        print("===========================================================================================")
        print(f"Your job started successfully! Started compute job with id: {job_id}")
        print("===========================================================================================")

        ## Check compute job status
        print(' ')
        print('Runing the compute job, this might take a while..., checking status every 20 sec.')
        succeeded = False
        for i in range(1, 200):
            print(f"--- Checking running status for {i} time ---")
            status = ocean.compute.status(DATA_ddo, compute_service, job_id, self.my_wallet)
            if status.get("dateFinished") and Decimal(status["dateFinished"]) > 0:
                succeeded = True
                break
            print(' ')
            print('C2D Still running, waiting for next check ...')
            print(' ')
            time.sleep(25)
        
        print(" ")
        print("=====================")
        print('Done! C2D successful.')
        print("=====================")
        temp = ocean.compute.compute_job_result_logs(
            DATA_ddo, compute_service, job_id, self.my_wallet
        )
        if temp:
            print(" ")
            print('Requesting the compute result ...')
            print("=================================")
            result = temp[0]
            print(type(result))
            print(result)
            print(' ')
            print(f"Compute job log ==> {result}")
            path = f"./c2d_output/{job_id}.pickle"

            ## 新建或者打开一个对应path路径上的文件，将返回的字节数据输出为文件（字节流转为文件流）
            with open(path, "wb") as file:
                file.write(result)
            print("========================================")
            print(f"Model is download at {path}")
            ## 获得文件后可在Jupyter上运行下面的代码
            # import pickle
            ## 这里pickles需要读取python对象，file.read()返回文件读取的内容，这里是bytes数据
            # with open('./c2d/xxx.txt', "rb") as file:
            #   model = pickle.loads(file)  # the gaussian model result
            #   assert len(model) > 0, "unpickle result unsuccessful"
        else:
            print(f"Result is empty, compute job finish unsuccessfully.")


    # def test_nft(self):
    #     model_key = 'model_key'
    #     model_value = 'model_value'
    #     data_nft = ocean.get_nft_token('0xaf5E5bC9f1f24dC5c1EF1301e2846A3BdD7Dc92E')
    #     data_nft.set_data('model_key', 'model_value', {"from": self.my_wallet})

    #     model_value1 = data_nft.get_data('name')
    #     print(f"Found that {model_key} = {model_value1}")


    ### Convert Notebook to C2D format Python script 
    def convert(self, file):
        import nbformat
        from jinja2 import Template
        # import os

        print('------------------------------------------')
        print('Converting notebook into Python script ...')

        # Load your Jupyter Notebook
        notebook_file = file
        with open(notebook_file, 'r', encoding='utf-8') as nb_file:
            notebook = nbformat.read(nb_file, as_version=4)

        # Collect content of 'train' cells
        train_content = ''
        for cell in notebook.cells:
            if 'train' in cell.metadata.tags:
                train_content += cell.source + '\n'
        
        input_content = ''
        for cell in notebook.cells:
            if 'input' in cell.metadata.tags:
                input_content += cell.source + '\n'
        
        import_content = ''
        for cell in notebook.cells:
            if 'import' in cell.metadata.tags:
                import_content += cell.source + '\n'

        # Load the Jinja2 template
        template_file = 'jupyterOcean/python_ocean/notebook_to_script.j2' 
        with open(template_file, 'r', encoding='utf-8') as template_file:
            template = Template(template_file.read())

        # Render the template
        resulting_script = template.render(nb=notebook, 
                                           train_content=train_content, 
                                           input_content=input_content,
                                           import_content=import_content
                                           )

        # Save the resulting Python script to a file
        script_file = 'ocean_algo.py'
        with open(script_file, 'w', encoding='utf-8') as script:
            script.write(resulting_script)
        
        print(' ')
        print('Convert finished ! ')
        print('------------------------------------------')


        # # Optionally, you can execute the generated script
        # os.system(f'python {script_file}')

