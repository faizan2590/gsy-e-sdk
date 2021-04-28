import logging
from time import sleep
from d3a_api_client.aggregator import Aggregator
from d3a_api_client.utils import get_area_uuid_from_area_name_and_collaboration_id, \
    get_sim_id_and_domain_names
from d3a_api_client.rest_market import RestMarketClient

# import logging
logger = logging.getLogger()
logger.disabled = False


class TestAggregator(Aggregator):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.is_finished = False
        self.fee_cents_per_kwh = 0

    def on_market_cycle(self, market_info):
        """
        market_info contains market_info dicts from all markets
        that are controlled by the aggregator
        """
        logging.info(f"AGGREGATOR_MARKET_INFO: {market_info}")
        if self.is_finished is True:
            return
        # if "content" not in market_info:
        # return

        grid_fee = [1, 2, 3]
        self.fee_cents_per_kwh += grid_fee[2]
        logging.info(f"{market_info}")
        # for area_event in market_info["content"]:
        for area_uuid, area_dict in self.latest_grid_tree_flat.items():
            # area_uuid = area_event["area_uuid"]
            if area_dict["area_name"] in market_names:
                if area_uuid is None:
                    continue
                self.add_to_batch_commands.grid_fees(
                    area_uuid=area_uuid, fee_cents_kwh=self.fee_cents_per_kwh)
        response = self.execute_batch_commands()
        logging.info(f"Batch command placed on the new market: {response}")

    def on_tick(self, tick_info):
        logging.debug(f"Progress information on the device: {tick_info}")

    def on_trade(self, trade_info):
        logging.debug(f"Trade info: {trade_info}")

    def on_finish(self, finish_info):
        self.is_finished = True


simulation_id, domain_name, websockets_domain_name = get_sim_id_and_domain_names()

aggr = TestAggregator(
    simulation_id=simulation_id,
    domain_name=domain_name,
    aggregator_name="test_aggregator",
    websockets_domain_name=websockets_domain_name
)

market_args = {
    "simulation_id": simulation_id,
    "domain_name": domain_name,
    "websockets_domain_name": websockets_domain_name
}
market_names = ["house 1"]
house_1_uuid = get_area_uuid_from_area_name_and_collaboration_id(
    market_args["simulation_id"], market_names[0], market_args["domain_name"])
market_args["area_id"] = house_1_uuid
house_1 = RestMarketClient(
    **market_args
)

house_1.select_aggregator(aggr.aggregator_uuid)
# house_2.select_aggregator(aggr.aggregator_uuid)

while not aggr.is_finished:
    sleep(0.5)
