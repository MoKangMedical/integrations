"""
MoKangMedical 集成中心 — 各项目的MCP/工具/数据源统一接入

用户视角：一个import就能调用所有外部数据源
"""

import json
import logging
import urllib.request
import urllib.parse
from typing import Dict, List, Optional

logger = logging.getLogger(__name__)


class IntegrationHub:
    """集成中心 — 统一数据源接入"""
    
    ENDPOINTS = {
        "clinicaltrials": {
            "name": "ClinicalTrials.gov",
            "url": "https://clinicaltrials.gov/api/v2/studies",
            "desc": "全球临床试验数据",
        },
        "pubmed": {
            "name": "PubMed",
            "url": "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi",
            "desc": "生物医学文献检索",
        },
        "chembl": {
            "name": "ChEMBL",
            "url": "https://www.ebi.ac.uk/chembl/api/data",
            "desc": "化合物和药物数据",
        },
        "opentargets": {
            "name": "OpenTargets",
            "url": "https://api.platform.opentargets.org/api/v4/graphql",
            "desc": "靶点验证数据",
        },
        "openfda": {
            "name": "OpenFDA",
            "url": "https://api.fda.gov/drug",
            "desc": "FDA药物审批和不良事件",
        },
        "omim": {
            "name": "OMIM",
            "url": "https://api.omim.org/api",
            "desc": "人类孟德尔遗传数据库",
        },
    }
    
    def search_clinical_trials(self, condition: str, max_results: int = 5) -> List[Dict]:
        """搜索临床试验"""
        params = urllib.parse.urlencode({
            "query.cond": condition,
            "pageSize": max_results,
            "format": "json"
        })
        url = f"{self.ENDPOINTS['clinicaltrials']['url']}?{params}"
        return self._fetch(url)
    
    def search_pubmed(self, query: str, max_results: int = 5) -> List[Dict]:
        """搜索PubMed文献"""
        params = urllib.parse.urlencode({
            "db": "pubmed",
            "term": query,
            "retmax": max_results,
            "retmode": "json"
        })
        url = f"{self.ENDPOINTS['pubmed']['url']}?{params}"
        result = self._fetch(url)
        return result if isinstance(result, list) else [result]
    
    def search_compounds(self, name: str) -> List[Dict]:
        """搜索ChEMBL化合物"""
        url = f"{self.ENDPOINTS['chembl']['url']}/molecule/search.json?q={name}&limit=5"
        return self._fetch(url)
    
    def get_target_info(self, symbol: str) -> Dict:
        """获取靶点信息（OpenTargets）"""
        query = {
            "query": """{
                target(ensemblId: "%s") {
                    id
                    approvedSymbol
                    approvedName
                    bioType
                }
            }""" % symbol
        }
        return self._fetch(self.ENDPOINTS['opentargets']['url'], data=json.dumps(query).encode())
    
    def _fetch(self, url: str, data: bytes = None) -> any:
        """统一HTTP请求"""
        try:
            req = urllib.request.Request(url, data=data, headers={"User-Agent": "MoKangMedical/1.0"})
            if data:
                req.add_header("Content-Type", "application/json")
            with urllib.request.urlopen(req, timeout=15) as resp:
                return json.loads(resp.read())
        except Exception as e:
            return {"error": str(e)}
    
    def list_integrations(self) -> Dict:
        """列出所有可用集成"""
        return {
            name: {"name": ep["name"], "desc": ep["desc"], "status": "available"}
            for name, ep in self.ENDPOINTS.items()
        }


if __name__ == "__main__":
    hub = IntegrationHub()
    print("🔗 MoKangMedical 集成中心")
    print(json.dumps(hub.list_integrations(), ensure_ascii=False, indent=2))
