from ScoutSuite.providers.aws.facade.base import AWSFacade
from ScoutSuite.providers.aws.resources.base import AWSResources
from ScoutSuite.core.console import print_exception


class Clusters(AWSResources):
    def __init__(self, facade: AWSFacade, region: str, vpc: str):
        super().__init__(facade)
        self.region = region
        self.vpc = vpc

    async def fetch_all(self):
        raw_clusters = await self.facade.redshift.get_clusters(self.region, self.vpc)
        for raw_cluster in raw_clusters:
            try:
                id, cluster = self._parse_cluster(raw_cluster)
                self[id] = cluster
            except Exception as e:
                print_exception('Failed to parse {} resource: {}'.format(self.__class__.__name__, e))

    def _parse_cluster(self, raw_cluster):
        name = raw_cluster.pop('ClusterIdentifier')
        raw_cluster['name'] = name
        raw_cluster['arn'] = 'arn:aws:redshift:{}:{}:cluster/{}'.format(self.region,
                                                                    self.facade.owner_id,
                                                                    name)

        return name, raw_cluster
