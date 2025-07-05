# explorer.py

import requests
import random
import time
import socket
from bs4 import BeautifulSoup


class Explorer:
    def __init__(self):
        self.headers = self._random_headers()
        self.targets = []
        self.mode = "stealth"  # Modes: stealth, aggressive, passive
        print("🛰️ Explorer module initialized.")

    def _random_headers(self):
        """Generate stealth headers to simulate different clients."""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            "Mozilla/5.0 (Linux; Android 11; SM-G981U)",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)",
            "Mozilla/5.0 (X11; Ubuntu; Linux x86_64)",
        ]
        return {
            "User-Agent": random.choice(user_agents),
            "Accept-Language": "en-US,en;q=0.9",
            "Connection": "keep-alive"
        }

    def search(self, query):
        """Perform an online search with stealth scraping."""
        try:
            print(f"🔍 Scouting target intel for: {query}")
            url = f"https://www.bing.com/search?q={query.replace(' ', '+')}"
            response = requests.get(url, headers=self.headers, timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.find_all('li', {'class': 'b_algo'})
            findings = []
            for r in results[:5]:
                title = r.find('h2')
                link = r.find('a')
                snippet = r.find('p') or r.find('div')
                if title and link:
                    findings.append({
                        'title': title.text.strip(),
                        'url': link['href'],
                        'summary': snippet.text.strip() if snippet else ''
                    })
            return findings
        except Exception as e:
            return f"⚠️ Explorer error: {e}"

    def scan_host(self, host):
        """Attempt basic connectivity & fingerprinting."""
        try:
            print(f"📡 Scanning host: {host}")
            ip = socket.gethostbyname(host)
            latency = self._ping_host(ip)
            return {
                "host": host,
                "ip": ip,
                "latency": f"{latency} ms" if latency else "Timeout"
            }
        except Exception as e:
            return f"⚠️ Scan failed: {e}"

    def _ping_host(self, ip):
        """Ping a host to check latency (Termux-compatible)."""
        try:
            result = os.popen(f"ping -c 1 {ip}").read()
            if "time=" in result:
                latency = result.split("time=")[-1].split(" ")[0]
                return latency
        except BaseException:
            return None

    def add_target(self, url):
        """Queue target for observation."""
        if url not in self.targets:
            self.targets.append(url)
            print(f"🎯 Target added: {url}")

    def watch_targets(self):
        """Monitor tracked URLs for changes or breaches."""
        reports = []
        for url in self.targets:
            try:
                print(f"🕵️ Watching {url}")
                response = requests.get(url, headers=self.headers, timeout=10)
                status = response.status_code
                content = response.text[:500]
                reports.append({
                    "url": url,
                    "status": status,
                    "snippet": content
                })
            except Exception as e:
                reports.append({
                    "url": url,
                    "error": str(e)
                })
        return reports

    def explore_deep(self, topic):
        """Perform an extended reconnaissance on a topic."""
        base = self.search(topic)
        intel = []
        for item in base:
            try:
                page = requests.get(
                    item["url"], headers=self.headers, timeout=10)
                soup = BeautifulSoup(page.text, 'html.parser')
                paragraphs = soup.find_all('p')
                content = ' '.join(p.text.strip() for p in paragraphs[:5])
                intel.append({
                    "source": item["url"],
                    "insight": content
                })
            except Exception as e:
                intel.append({
                    "source": item["url"],
                    "error": str(e)
                })
        return intel

    def analyze_trends(self, keyword):
        """Analyze online trends, headlines, and sentiment."""
        headlines = self.search(f"{keyword} news")
        trends = [h['title'] for h in headlines if 'title' in h]
        return {
            "keyword": keyword,
            "trend_count": len(trends),
            "examples": trends
        }

    def cloak(self):
        """Change headers and network identity to stay hidden."""
        self.headers = self._random_headers()
        print("🕶️ Explorer has cloaked identity.")
