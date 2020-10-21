from ScoutSuite.providers.azure.facade.base import AzureFacade
from ScoutSuite.providers.azure.resources.base import AzureResources
from ScoutSuite.core.console import print_exception


class Alerts(AzureResources):

    def __init__(self, facade: AzureFacade, subscription_id: str):
        super().__init__(facade)
        self.subscription_id = subscription_id

    async def fetch_all(self):
        for raw_alert in await self.facade.securitycenter.get_alerts(self.subscription_id):
            try:
                id, alert = self._parse_alert(raw_alert)
                self[id] = alert
            except Exception as e:
                print_exception('Failed to parse {} resource: {}'.format(self.__class__.__name__, e))

    def _parse_alert(self, alert):
        alert_dict = {}
        alert_dict['id'] = alert.id
        alert_dict['name'] = alert.name
        return alert_dict['id'], alert_dict
