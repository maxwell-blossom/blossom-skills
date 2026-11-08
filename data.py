# Seed catalogue for Blossom Skills V1. Creators other than @blossom, @beevis and @maxstocks are invented.
CREATORS = {
 'blossom':   dict(name='Blossom', handle='blossom', badge='official', bio='Official skills and MCPs from the Blossom team.', followers=512000, color='#7361F7', initials='B', photo='avatar_12.jpg'),
 'beevis':    dict(name='Beevis', handle='beevis', badge='official', bio="Blossom's AI investing coach. Roasts and coaches, in that order.", followers=88400, color='#2323B3', initials='🐝', beevis=True),
 'maxstocks': dict(name='Max Nicholson', handle='maxstocks', badge='verified', bio='CEO @ Blossom. Dividend investor, TFSA maxer, ETF nerd. 🇨🇦', followers=41200, color='#35C7B2', initials='MN', photo='avatar_01.jpg'),
 'dividendsdan': dict(name='Dividends Dan', handle='dividendsdan', badge='ambassador', bio='Living off dividends since 2021. I share the actual numbers.', followers=68900, color='#12BD57', initials='DD', photo='avatar_09.jpg'),
 'tfsa_tina': dict(name='Tina Kowalski', handle='tfsa_tina', badge='verified', bio='CPA by day. TFSA, RRSP and FHSA room are my love language.', followers=23700, color='#FF7733', initials='TK', photo='avatar_08.jpg'),
 'northofthe49': dict(name='North of the 49', handle='northofthe49', badge='ambassador', bio='Canadian banks, pipelines and rails. Boring is beautiful.', followers=34100, color='#E70037', initials='N49', photo='avatar_04.jpg'),
 'quantqueen': dict(name='Priya Raman', handle='quantqueen', badge='verified', bio='Ex-risk desk. I build tools so you don’t blow up.', followers=19800, color='#4D35EB', initials='PR', photo='avatar_10.jpg'),
 'earningsedge': dict(name='Earnings Edge', handle='earningsedge', badge='pro', bio='Reads every 10-K so you don’t have to. Fundamentals only.', followers=15600, color='#018FBF', initials='EE', photo='avatar_05.jpg'),
 'satoshi_sam': dict(name='Sam Okafor', handle='satoshi_sam', badge='pro', bio='Crypto is 5% of my portfolio and 50% of my DMs.', followers=27300, color='#F6C000', initials='SO', photo='avatar_06.jpg'),
 'anthony.invests': dict(name='Anthony Holstein', handle='anthony.invests', badge='verified', bio='Data @ Blossom. 21 yo aerospace technician and engineering student 🚀 Space stocks: LUNR, MDA, PL. 🇨🇦 YUL', followers=8167, color='#2323B3', initials='AH', photo='anthony.jpg'),
 'piiverse': dict(name="Perry's PIIverse", handle='piiverse', badge='ambassador', bio='Retired Sep’23. ~$1.7M across 4 RIFs and 2 TFSAs, $30K+/month of income from 39 covered-call ETFs. YouTube: @PIIverse. 🇨🇦 Winnipeg', followers=12000, color='#12BD57', initials='PP', photo='perry.jpg'),
 'rebalancer_rob': dict(name='Robin Chen', handle='rebalancer_rob', badge='verified', bio='Index funds, rebalancing, and a spreadsheet for everything.', followers=9400, color='#409082', initials='RC', photo='avatar_03.jpg'),
}

MCPS = [
 dict(id='blossom-connector', kind='mcp', emoji='🔗', name='Blossom Connector', creator='blossom', status='',
      pitch='Connect Blossom to Claude, ChatGPT, Grok or Cursor. Your portfolio, trades and watchlist, plus the posts, discussions and people you follow — the same read access Beevis has inside the app.',
      installs=4820, rating=4.8, ratings=212, updated='2026-11-07', version='0.10.0', price='Requires Blossom PRO+ · included with your subscription',
      url='https://mcp.blossomsocial.com/connector', auth='OAuth · sign in with your Blossom account',
      tools=[('get_portfolio','Your linked portfolio: positions, weights, cost basis, day and total P&L.'),
             ('get_holdings','Positions for one account or all, with sector, country and asset type.'),
             ('get_trades','Your trades for a date range, with price, quantity and realised P&L.'),
             ('get_watchlist','Tickers you watch, with your notes.'),
             ('get_following_activity','What the investors you follow bought and sold this week (what they chose to share).'),
             ('get_dividends','Upcoming and received dividends for your holdings.'),
             ('get_profile','Your public profile, badges and investing style from the Beevis survey.'),
             ('get_feed','Your OneFeed: the posts Blossom would show you right now, with the ticker, trade and reactions on each.'),
             ('get_ticker_posts','What investors are saying about a ticker — recent posts, the trades attached to them, reaction mix, and the most-liked takes.'),
             ('search_posts','Full-text search across Blossom posts, by ticker, topic, creator or date range.'),
             ('get_post','One post in full, with its comments, the poster\'s linked trade and whether they still hold it.'),
             ('get_my_posts','Your own posts and comments, with how they performed.')],
      about='Included with Blossom PRO+ — sign in with a PRO+ account and it works; no separate charge. The Connector is read-only. Posts come through the same way Beevis reads them in the app — public posts only, with the poster\'s handle, so a skill can cite who said what and link back to the post. It never places orders and never sees your brokerage login — it reads the same data Blossom already shows you, through the same SnapTrade link. Revoke it any time from Settings → Connected apps.',
      log=[('0.10.0','2026-11-07','Posts: get_feed, get_ticker_posts, search_posts, get_post, get_my_posts — the same read access Beevis has in the app.'),('0.9.2','2026-11-04','Added get_dividends. get_portfolio now returns weights to 2 decimals.'),('0.9.1','2026-10-21','OAuth flow works from ChatGPT developer mode.'),('0.9.0','2026-10-07','First beta. Claude and Cursor.')]),
 dict(id='blossom-trade-data', kind='mcp', emoji='📊', name='Blossom Aggregate Trade Data', creator='blossom', status='',
      pitch='What 500,000+ investors are buying, selling and holding — crowd flows by ticker, sector, theme, region and portfolio size, updated daily.',
      installs=2140, rating=4.7, ratings=96, updated='2026-11-06', version='0.4.0', price='$19/mo · $149/yr · paid, no free tier',
      url='https://mcp.blossomsocial.com/trade-data', auth='API key from Settings → Developer, or OAuth',
      tools=[('crowd_flows','Net $ bought/sold and headcount by ticker for a day or week, by region.'),
             ('trending_tickers','Most-bought and most-sold by investors, vs the 4-week average.'),
             ('sector_flows','Flows by GICS sector and by Blossom theme (AI chips, Memes, Canadian blue chips…).'),
             ('ticker_history','12 weeks of flows for one ticker, with first-time buyers and dormant sellers.'),
             ('anomalies','Tickers trading unusually vs their own history — the spike detector behind the share cards.'),
             ('millionaire_flows','What $1M+ portfolios bought and sold this week.'),
             ('sentiment','Post volume and reaction mix for a ticker, 7 and 30 days.')],
      about='Paid MCP: $19/month or $149/year, billed by Stripe, cancel anytime. Aggregates only: no user is identifiable, every row is at least 20 accounts, and whale rows are capped so one account can’t move a number. The same feed the Blossom share cards and the Weekly Buzz are built on.',
      log=[('0.4.0','2026-11-06','anomalies tool: 12-week baselines, first-time buyer share.'),('0.3.0','2026-10-24','Regions: All, Canada, US, UK.'),('0.2.0','2026-10-10','sector_flows with Blossom themes.')]),
 dict(id='fiscal-ai', kind='mcp', emoji='🧮', logo='fiscal_logo_96.png', name='Fiscal.ai', creator=None, creator_name='Fiscal.ai', third_party=True, status='Partner',
      pitch='Financial statements, ratios, estimates, segments, filings and prices for 100,000+ companies. The fundamentals layer for any skill.',
      installs=1380, rating=4.9, ratings=58, updated='2026-11-01', version='—', price='$49.99/mo · billed by Fiscal.ai',
      url='https://api.fiscal.ai/mcp', auth='OAuth in the browser, or an API key as a Bearer header',
      tools=[('financial statements','As-reported and standardized, quarterly and annual.'),('ratios & adjusted metrics','Margins, returns, leverage, valuation.'),('estimates','Consensus revenue and EPS.'),('segments & KPIs','Revenue by segment and company-specific KPIs.'),('filings','10-K, 10-Q, 8-K and international equivalents.'),('prices','Daily history and quotes.')],
      about='Built by Fiscal.ai. $49.99/month, billed by Fiscal.ai on fiscal.ai — Blossom lists it so skills can declare it as a requirement; your Fiscal plan decides coverage and rate limits. Works in Claude (one-click connector), Claude Code, Cursor and ChatGPT developer mode.',
      log=[('—','2026-11-01','Listed on Blossom Skills.')]),
 dict(id='public-mcp', kind='mcp', compat=True, country='US', logo='public_logo_96.png', emoji='🅿️', name='Public.com', creator=None, creator_name='Public.com', third_party=True, status='Broker', trades=True,
      pitch='Your Public.com brokerage account as tools: portfolio, orders, real-time quotes, options chains and Greeks, tax lots — and order placement, if you turn it on.',
      installs=640, rating=4.6, ratings=23, updated='2026-10-28', version='0.3.0', price='Free · needs a Public.com account and API key',
      url='uvx publicdotcom-mcp-server', auth='API key from Public.com → Settings → API (PUBLIC_COM_SECRET); remote mode sends it as a Bearer header',
      tools=[('get_portfolio','Positions, equity, buying power, open orders.'),('get_quotes','Real-time quotes for stocks, crypto and options.'),('get_option_chain / get_option_greeks','Chains, expirations and Greeks.'),('get_tax_lots','Unrealised gain/loss by lot.'),('preflight_order','Estimate cost and impact before an order.'),('place_order ⚠️','Places real single-leg orders; multi-leg and spread variants too. Modifies your account.')],
      about='Published under the PublicDotCom GitHub organisation (Apache 2.0). Runs locally with your API key, or remotely over streamable HTTP. Blossom lists it so skills can declare it — Blossom-distributed skills stay read-only, so a skill may read quotes and positions from it but never call the order tools.',
      log=[('0.3.0','2026-10-28','Listed on Blossom Skills. Options Greeks and tax-lot tools.')]),
 dict(id='questrade-mcp', kind='mcp', compat=True, country='Canada', logo='questrade_logo_96.png', emoji='🍁', name='Questrade', creator=None, creator_name='Community', third_party=True, status='Broker',
      pitch='Read-only access to your Questrade accounts: portfolio, positions, balances, quotes, price history, orders and activity. No order placement.',
      installs=410, rating=4.5, ratings=17, updated='2026-10-15', version='—', price='Free · needs a Questrade API refresh token',
      url='node dist/index.js  (http: localhost:3100/mcp)', auth='Questrade API Hub refresh token (QUESTRADE_REFRESH_TOKEN); stored encrypted, renewed automatically',
      tools=[('getPortfolio','All accounts, positions and balances.'),('getPositions / getBalances','Per-account positions, cash and buying power.'),('getQuotes / lookupSymbol','Level 1 quotes (delayed without a market-data subscription).'),('getPriceHistory','OHLCV candles, 1-minute to yearly.'),('getOrders / getAccountActivity','Order history and executions.')],
      about='Community-built TypeScript server, proprietary licence, Node 22+. Read-only by design — the author ships no trade-placement tools. Listed as a Blossom partner-style MCP so Canadian skills can declare it.',
      log=[('—','2026-10-15','Listed on Blossom Skills.')]),
 dict(id='robinhood-mcp', kind='mcp', compat=True, logo='robinhood_logo_96.png', emoji='🪶', name='Robinhood', creator=None, creator_name='Robinhood (official)', third_party=True, status='Broker', trades=True, country='US',
      pitch='Robinhood’s own remote MCP: reads every account you have (positions, balances, order history) and trades stocks, options and crypto in a dedicated agent account.',
      installs=1240, rating=4.5, ratings=52, updated='2026-10-09', version='—', price='Free · needs a Robinhood account in good standing',
      url='https://agent.robinhood.com/mcp/trading', auth='OAuth · signing in opens a dedicated MCP account; trade approvals are off by default (turn them on under Agent Settings → Safety Controls)',
      tools=[('accounts & positions','All your Robinhood accounts: positions, balances, full order history.'),('quotes','Stock, option and crypto quotes.'),('place_order ⚠️','Market (shares or dollars), limit, stop-limit and stop-market orders in the MCP account. Real money.'),('options & crypto ⚠️','Options orders; crypto if you have Robinhood Crypto and accept the updated agreement.')],
      about='First-party, built by Robinhood. Trades only happen in the separate MCP account it creates for you; reads cover everything. Robinhood says it does not supervise or audit the agents you connect. US only.',
      log=[('—','2026-10-09','Listed on Blossom Skills.')]),
 dict(id='webull-mcp', kind='mcp', compat=True, logo='webull_logo_96.png', emoji='🐂', name='Webull', creator=None, creator_name='Webull (official)', third_party=True, status='Broker', trades=True, country='US',
      pitch='Webull’s official MCP on top of its OpenAPI: real-time quotes, balances and positions, and placing, changing and cancelling orders in plain language.',
      installs=760, rating=4.4, ratings=29, updated='2026-06-11', version='—', price='Free · needs a Webull account and OpenAPI keys',
      url='developer.webull.com → AI-friendly resources → MCP', auth='Webull OpenAPI app key and secret; the hosted version is read-only, the local server trades (sandbox by default)',
      tools=[('quotes','Real-time market data.'),('account','Balances, positions, order history and order details.'),('place / modify / cancel order ⚠️','Order management through OpenAPI. Real money outside the sandbox.')],
      about='Launched June 2026 for all US clients; Webull says other markets follow. Canada not yet. Read-only through the hosted server, trading through the local one.',
      log=[('—','2026-06-11','Listed on Blossom Skills.')]),
 dict(id='moomoo-mcp', kind='mcp', compat=True, logo='moomoo_logo_96.png', emoji='🐮', name='moomoo', creator=None, creator_name='moomoo (official skills) · community MCP', third_party=True, status='Broker', trades=False, country='US',
      pitch='moomoo’s Agent Skills route (open.moomoo.com) plus a community MCP: quotes, candles, order book, accounts, positions, cash flow and order history. Simulated account by default.',
      installs=330, rating=4.2, ratings=14, updated='2026-10-30', version='—', price='Free · needs a moomoo account; the community MCP needs OpenD running',
      url='moomoo-mcp (Go binary) + OpenD on 127.0.0.1:11111', auth='Your moomoo login through OpenD; REAL-account reads need a trade password, order placement is not implemented',
      tools=[('market data','get_stock_quote, get_market_snapshot, get_historical_klines, get_order_book.'),('account','get_accounts, get_assets, get_positions, get_account_summary, get_cash_flow.'),('orders (read)','get_orders, get_deals, history. No place_order.')],
      about='moomoo publishes skills and an MCP guide for Claude at open.moomoo.com and moomoo SkillHub; the standalone MCP is community-built (iwanbk/moomoo-mcp) and read-only. Markets: US, HK, SG, JP, CN. Canada not confirmed.',
      log=[('—','2026-10-30','Listed on Blossom Skills.')]),
 dict(id='ibkr-mcp', kind='mcp', compat=True, logo='ibkr_logo_96.png', emoji='🅸', name='Interactive Brokers', creator=None, creator_name='Interactive Brokers (official)', third_party=True, status='Broker', trades=False, country='US · International',
      pitch='IBKR’s own hosted connector for Claude, ChatGPT and Grok: positions, cash, margin, P&L, transactions, option chains and risk across every account — and it drafts orders you submit yourself.',
      installs=1980, rating=4.7, ratings=88, updated='2026-06-22', version='—', price='Free · needs an IBKR account',
      url='Claude → Settings → Connectors → Interactive Brokers (IBKR) → Connect', auth='Your IBKR login in the browser; no API keys',
      tools=[('portfolio','Positions, cash, margin, realised and unrealised P&L, multi-currency balances, linked accounts.'),('history','Transactions, 30 days of prices, real-time snapshots.'),('options & risk','Option chains, risk exposures.'),('draft_order','Builds market/limit orders (stocks, ETFs, options, futures) into IBKR’s “AI Instructions” tab — you convert them to live orders in IBKR. Never submits to market.')],
      about='First-party, launched June 2026. The safest trading route on this list because the human always submits. Works for Canadian IBKR accounts too.',
      log=[('—','2026-06-22','Listed on Blossom Skills.')]),
 dict(id='alpaca-mcp', kind='mcp', compat=True, logo='alpaca_logo_96.png', emoji='🦙', name='Alpaca', creator=None, creator_name='Alpaca (official)', third_party=True, status='Broker', trades=True, country='US',
      pitch='Alpaca’s official MCP server: account, positions, market data and order placement, with paper trading on by default.',
      installs=1120, rating=4.6, ratings=41, updated='2026-09-15', version='—', price='Free · needs Alpaca API keys',
      url='alpaca-mcp-server (local)', auth='Alpaca API key and secret; ALPACA_PAPER_TRADE=true by default, ALPACA_TOOLSETS limits what the agent can touch',
      tools=[('account & positions','Balances, positions, P&L.'),('market data','Quotes, bars, news.'),('place_order ⚠️','Stocks, ETFs, options and crypto. Paper by default; live when you flip it.')],
      about='First-party. The paper-trading default makes it the easiest broker to test a trading skill against. US.',
      log=[('—','2026-09-15','Listed on Blossom Skills.')]),
]


def md(s): return s.strip('\n')

SKILLS = [
 dict(id='space-stock-lens', highlights=['Every space name you hold or watch, on Anthony’s forward price-to-sales ladder', 'Backlog, cash and the milestones since the last high — did the business or the price move?', 'De-SPAC history: which names already survived a 50–80% drawdown', 'Canadian? Flags the CDR when one exists'], emoji='🚀', name='Space Stock Lens by Anthony', creator='anthony.invests', cat='Research',
      pitch='Anthony’s way of reading space stocks — forward price-to-sales across the sector, backlog vs price, and what the company actually shipped since its high — run on the names you hold or watch.',
      downloads=1860, rating=4.9, ratings=74, updated='2026-11-05', version='1.3.0', requires=['blossom-connector','fiscal-ai'], optional=['blossom-trade-data'],
      price=dict(monthly=4.99, yearly=39), cadence='Monthly, and after every space-sector earnings week',
      prompts=['Run the space lens on my portfolio', 'Is LUNR cheap or just down? Use Anthony’s lens', 'Compare RKLB, ASTS, LUNR and MDA on forward sales'],
      sample='**🚀 Space lens · your names: LUNR, MDA, PL · watch: RKLB, ASTS, KRMN**\n\n| Name | Fwd P/S | Backlog | Net cash | Since 52-wk high | Verdict |\n|---|---|---|---|---|---|\n| **LUNR** | 2.2× | $1.76B (was $213M) | +$367M | −80% | business up, price down |\n| **MDA** | 3.4× | $3.9B | +$1.3B | −31% | priced like a contractor, growing like a platform |\n| **PL** | 6.1× | $0.7B | +$0.2B | −12% | fair; watch margins |\n| **RKLB** | ~50× | $1.1B | +$0.5M | −18% | priced for Neutron working first time |\n| **ASTS** | ~135× | pre-revenue | +$0.9B | −22% | a story, not a multiple |\n\n**LUNR** — the gap between the business and the price is the widest in the sector. Since the May 28 high: 6th CLPS mission ($148M), 18 spacecraft for L3Harris, $600M+ comms program, Lanteris closed (revenue 4×), two NASA Earth-science wins, SXM-11 delivered. Management still guides positive adj. EBITDA. The −80% is macro and the SPCX IPO pulling money out of the sector, not the company. *Anthony on Blossom, Nov 5: “$LUNR that once was at the same valuation a year ago did not have Lanteris… yet its share price has fallen more than 80%.”* → [post](https://www.blossomsocial.com/users/Anthony-Holstein__Wzsbh4hcwoeoMZZm)\n\n**De-SPAC check:** RKLB and ASTS both lost 50–80% between 2021 and 2023 before the 2024 run; LUNR is in that phase now. That is the pattern, not the exception.\n\n🇨🇦 **CDRs:** RKLB has a CIBC CDR (RKLB.NE, CAD-hedged). LUNR and ASTS don’t — you’re taking USD exposure.\n\n*Not a recommendation. This is Anthony’s framework applied to your holdings; he holds LUNR (41% of his portfolio) and MDA.*',
      log=[('1.3.0','2026-11-05','Adds the “since the high” milestone list and the de-SPAC pattern check.'),('1.2.0','2026-10-20','CDR flag for Canadian users (RKLB CDR launched).'),('1.1.0','2026-10-02','Backlog column from the latest quarter via Fiscal.ai.'),('1.0.0','2026-09-10','First release: the forward P/S ladder.')],
      reviews=[('maxstocks',5,'This is the post he writes every month, but on my holdings. Exactly what the marketplace is for.'),('quantqueen',5,'The P/S ladder is brutal and correct. ASTS at 135× says it all.'),('earningsedge',4,'Want it to pull the 10-Q backlog number itself when Fiscal doesn’t have it.')],
      skill=md('''
---
name: space-stock-lens
description: Anthony Holstein's (@anthony.invests) framework for reading space and space-infrastructure stocks — forward price-to-sales across the sector, backlog and cash vs price, milestones since the last high, de-SPAC drawdown history, and CDR availability for Canadians — applied to the user's holdings and watchlist. Use when the user asks about space stocks, LUNR, RKLB, ASTS, MDA, PL, KRMN, or "is this space stock cheap or just down".
---

# Space Stock Lens (by Anthony, @anthony.invests)

You are applying one investor's method, not giving advice. Say so at the end, and say what he holds.

## Needs
- Blossom Connector MCP: `get_holdings`, `get_watchlist`, `get_ticker_posts`
- Fiscal.ai MCP: revenue guidance, backlog, cash, market cap
- Optional — Blossom Aggregate Trade Data MCP: `crowd_flows` (what Blossom investors did this week)

## The universe
Space infrastructure and launch: LUNR, MDA, RKLB, ASTS, PL, KRMN, RDW, BKSY, SPIR, LMT/NOC/RTX only if the user holds them (defence, not space). Add anything in the user's holdings or watchlist that Fiscal classifies as aerospace. Ignore SPCX (it is the ETF that pulled flows from the names — mention it as a reason, not a row).

## Steps
1. Pull holdings and watchlist; keep the universe above. If the user holds none, run it on LUNR, MDA, RKLB, ASTS, PL and say so.
2. For each name: forward price-to-sales = market cap (all share classes) ÷ midpoint of management's current-year revenue guidance (or next-12-month consensus). Backlog and net cash from the latest quarter. Drawdown from the 52-week high.
3. "Since the high": list what the company announced since its 52-week high — contracts with dollar values, acquisitions closed, missions delivered, guidance changes. Dated, one line each. This is the heart of the method: did the business move, or only the price?
4. De-SPAC check: for any name that came public by SPAC in 2021–2023, note the 2021–2023 drawdown and the 2024 recovery, so the user sees the pattern.
5. Canadians (country = CA): flag whether a CIBC CDR exists for the name.
6. Pull the most-liked Blossom post on each held name from the last 30 days and quote one line with the handle and a link.

## Output
One table: Name | Fwd P/S | Backlog | Net cash | Since 52-wk high | Verdict (five words max, Anthony's voice: "business up, price down", "priced for Neutron working first time"). Then one paragraph per held name with the "since the high" list. Then the CDR line. Then the disclosure.

## Rules
- Verdicts describe valuation and progress. Never "buy", "sell" or "add".
- Every number has a date and a source (Fiscal.ai or the company release).
- Disclosure line, always: this is Anthony's framework; he holds LUNR and MDA; not a recommendation.
'''),
 ),
 dict(id='piiverse-income-rules', highlights=['Your income portfolio graded against Perry’s written rules, one line per rule', 'Monthly, weekly and pay-alignment days: what actually lands in your account and when', 'Cash reserve vs his 5% target, and what the next distributions rebuild', 'NAV-indifference check: are you reacting to price or to income?'], emoji='💰', name='PIIverse Income Rules Check', creator='piiverse', cat='Dividends',
      pitch='Perry’s written investment rules — the ones he retired on — run against your income portfolio: what passes, what breaks a rule, what your income actually pays this month, and whether you’re living by NAV or by income.',
      downloads=3120, rating=4.9, ratings=141, updated='2026-11-06', version='2.0.0', requires=['blossom-connector'], optional=['blossom-trade-data','questrade-mcp'],
      price=dict(monthly=6.99, yearly=59), cadence='Monthly, after Perry’s month-in-review video',
      prompts=['Run my portfolio through Perry’s income rules', 'What does my income portfolio pay this month, by week?', 'Am I reacting to NAV or to income? Be honest'],
      sample='**💰 PIIverse rules check · 23 holdings · income portfolio $412K**\n\n| # | Perry’s rule | You | |\n|---|---|---|---|\n| 1 | Income first: every holding must pay monthly or weekly | 21 of 23 do — **CNQ** and **ENB** pay quarterly | ⚠️ |\n| 2 | No single fund over 10% of the income portfolio | **HHIS** is 12.4% | ⚠️ |\n| 3 | Keep a 5% cash reserve; let distributions rebuild it | 2.1% — you spent it on the dip | ⚠️ |\n| 4 | Know the yield *and* the NAV trend of every CC fund | 4 funds you can’t explain the NAV path for: MSTY, CONY, YBIT, USOY | ⚠️ |\n| 5 | NAV indifference: judge by income paid, not price | you sold **BANK** on a −6% day; it had paid every month | ❌ |\n| 6 | Separate growth sleeve from income sleeve | mixed in one account — CVE and HWX sit beside the income funds | ⚠️ |\n| 7 | Write the rule down before you break it | — | ✅ you’re here |\n\n**This month pays $2,870:** week 1 $410 · week 2 $1,230 (Canadian monthlies + the semi-monthlies) · week 3 $560 · week 4 $670. **Nov 7 is a pay-alignment day** — 14 of your funds landed together. Your reserve is back to 5% after week 2 if you don’t touch it.\n\n**The honest line (rule 5):** three of your last five trades were sells on red days in funds that kept paying. Perry’s test is simple — did the income stop? It didn’t. *Perry on Blossom, Nov 6: “even when bloodbaths on the markets… INCOME KEEPS PAYING OUT… I haven’t realized ANY LOSS.”* → [post](https://www.blossomsocial.com/users/Perrys-PIIverse__e8gvPgBKi9R2SN5c)\n\n*Perry’s rules, your portfolio. He runs ~$1.7M this way and holds MSTY, HHIS, BANK and ENCL; this is not a recommendation.*',
      log=[('2.0.0','2026-11-06','Rules updated to Perry’s current list (single-stock rule retired; growth-sleeve rule added after the ATH rebalance). Pay-alignment days.'),('1.4.0','2026-10-15','Weekly-payer ETFs (US CC weeklies) in the pay calendar.'),('1.2.0','2026-09-22','Cash-reserve rebuild estimate from next month’s distributions.'),('1.0.0','2026-08-28','First release: the seven rules.')],
      reviews=[('dividendsdan',5,'The NAV-indifference line hurt. In a good way.'),('maxstocks',5,'This is Perry’s pinned post made executable. 212K views on the post for a reason.'),('tfsa_tina',4,'Would love the RRIF minimum-withdrawal math for the retirees.')],
      skill=md('''
---
name: piiverse-income-rules
description: Runs the user's income portfolio through Perry's (@piiverse) written investment rules — monthly/weekly payers, position caps, a 5% cash reserve, NAV indifference, separate growth and income sleeves — and builds the month's pay calendar. Use when the user asks about income investing, covered-call ETFs, their cash reserve, pay-alignment days, or "am I reacting to NAV".
---

# PIIverse Income Rules Check (by Perry, @piiverse)

Perry retired in September 2023 on a derivative-based passive income portfolio and wrote his rules down so he would notice when he broke them. This skill does the noticing, for the user's portfolio.

## Needs
- Blossom Connector MCP: `get_holdings`, `get_dividends`, `get_trades`, `get_ticker_posts`
- Optional — Blossom Aggregate Trade Data MCP: `crowd_flows` (what other income investors did on the same red day)
- Optional — Questrade MCP: per-account balances for the cash-reserve line, if the user's cash sits outside the linked Blossom accounts

## Perry's rules (current list — update when he updates the pinned post)
1. Income first: every income-sleeve holding pays monthly or weekly.
2. No single fund over 10% of the income sleeve.
3. Keep a 5% cash reserve; let distributions rebuild it, don't top it up by selling.
4. Know the yield and the NAV trend of every covered-call fund you own; if you can't explain the NAV path, you don't own it, it owns you.
5. NAV indifference: judge a holding by the income it paid, not the price today.
6. Growth money is separate from income money — different sleeve, different rules.
7. Write the rule down before you break it.

## Steps
1. `get_holdings`. Split income sleeve (anything that pays monthly/weekly, covered-call ETFs, high-yield funds) from growth sleeve (single stocks, non-paying ETFs). Say which is which.
2. Grade each rule: ✅ pass, ⚠️ bends it, ❌ breaks it — one line each with the specific holding and number.
3. `get_dividends` for the current month: total, by week. Flag pay-alignment days (3+ funds paying the same day).
4. Cash reserve as a % of the income sleeve; estimate when distributions bring it back to 5%.
5. `get_trades` last 90 days: for every sell on a down day, check whether the fund's distribution was cut. If not, it's a rule-5 miss. Count them. Be direct.
6. Quote one line from Perry's most recent relevant post with the link.

## Output
The seven-row table, the pay calendar paragraph, the honest rule-5 paragraph, the disclosure.

## Rules
- Never recommend a fund. Grade the portfolio the user has.
- Numbers come from Blossom; say "manually added" if the holding is.
- Disclosure, always: Perry's rules, the user's portfolio; what Perry holds; not a recommendation.
'''),
 ),
 dict(id='earnings-season-checklist', shots=[('earnings_1.jpg', 'The next 14 days, with consensus and what holders on Blossom did')], highlights=['Every holding reporting in the next 14 days, by date', "Consensus EPS and last quarter's reaction per name", 'What investors who hold it did after last earnings', 'Warns when >20% of your portfolio reports within 48h'], emoji='🧾', name='Earnings Season Checklist', creator='maxstocks', cat='Earnings',
      pitch='Every holding reporting in the next 14 days, what the Street expects, and what investors who hold it did last quarter.',
      downloads=8410, rating=4.9, ratings=437, updated='2026-11-03', version='1.4.0', requires=['blossom-connector','blossom-trade-data'],
      price=dict(free=True), cadence='Each earnings season',
      prompts=['Run my earnings checklist', 'Which of my holdings report this week?', 'What did Blossom investors do with NVDA after last earnings?'],
      sample='**📅 Next 14 days · 6 of your 23 holdings report**\n\n| Date | Ticker | Weight | Consensus EPS | Last qtr reaction | Investors who hold it did |\n|---|---|---|---|---|---|\n| Nov 12 | SHOP | 8.1% | $0.42 | −9% on a miss | Net **bought** (first time in 7 wks) |\n| Nov 13 | AAPL | 11.4% | $2.31 | +2% | Held |\n| Nov 19 | NVDA | 6.2% | $1.24 | −4% despite beat | Net **sold**, 62% buys → 21% |\n\n⚠️ 25% of your portfolio reports within 48 hours of each other (Nov 12–13).',
      log=[('1.4.0','2026-11-03','Adds the "what investors who hold it did" column from the Aggregate Trade Data MCP.'),('1.3.0','2026-10-15','Flags earnings clusters (>20% of portfolio reporting within 48h).'),('1.2.0','2026-09-28','Consensus from Fiscal.ai when connected; falls back to the Blossom quote.'),('1.0.0','2026-08-30','First release.')],
      reviews=[('dividendsdan',5,'Ran it Sunday night, had my week planned in 30 seconds. The cluster warning saved me on SHOP/AAPL.'),('tfsa_tina',5,'The "what investors who hold it did" column is the best thing on this site.'),('rebalancer_rob',4,'Great. Wish it could export to a calendar.')],
      skill=md('''
---
name: earnings-season-checklist
description: Lists every holding in the user's Blossom portfolio reporting earnings in the next 14 days with consensus expectations, last quarter's reaction and what Blossom investors who hold it did. Use when the user asks about earnings, "what reports this week", or to prepare for earnings season.
---

# Earnings Season Checklist

You help a Blossom investor prepare for earnings season. Be concrete, use their real holdings, and never guess a date or a number you did not get from a tool.

## Needs
- Blossom Connector MCP: `get_portfolio`, `get_holdings`
- Blossom Aggregate Trade Data MCP: `ticker_history`
- Optional: Fiscal.ai MCP for consensus estimates. If it is not connected, say "consensus unavailable" rather than inventing one.

## Steps
1. Call `get_portfolio`. Keep tickers with weight ≥ 1%.
2. For each, find the next earnings date (Fiscal.ai `estimates` if connected, otherwise the company's last announced date pattern; label it "estimated").
3. Keep tickers reporting within 14 days. Sort by date.
4. For each: consensus EPS and revenue (if available), last quarter's one-day reaction, and `ticker_history` for the week after last quarter's report — summarise as "net bought / net sold / held" with the buy share vs usual.
5. Flag clusters: if holdings totalling more than 20% of the portfolio report within 48 hours, add a ⚠️ line.
6. Output the table below, then one line per flagged cluster, then "Nothing else reports in the window." if the list is short.

## Output
| Date | Ticker | Weight | Consensus EPS | Last qtr reaction | Investors who hold it did |

Keep it to the table and the flags. No advice on whether to buy or sell — the user decides.
'''),
 ),
 dict(id='dividend-income-planner', shots=[('dividend_1.jpg', 'Monthly income timeline and income by holding'), ('dividend_2.jpg', 'Ex-dividend calendar with what you get, and Beevis’s two flags')], highlights=['Month-by-month dividend bars for the next 12 months', 'Cut-risk flags from payout ratio and dividend history', 'Yield on cost and the holdings carrying the income', '“How much do I need in X for $500/mo” calculator'], emoji='💸', name='Dividend Income Planner', creator='dividendsdan', cat='Dividends',
      pitch='Your next 12 months of dividends, month by month, with cut risk flagged and the three holdings doing the heavy lifting.',
      downloads=5230, rating=4.8, ratings=268, updated='2026-11-01', version='2.1.0', requires=['blossom-connector'],
      price=dict(monthly=4.99, yearly=39), cadence='Monthly, after the ex-div calendar updates',
      prompts=['Plan my dividend income for the next 12 months', 'Which of my dividends are at risk of a cut?', 'How much do I need in VDY to cover $500/month?'],
      sample='**💸 Next 12 months: $6,284 (≈ $524/mo)** · yield on cost 4.1%\n\n```\nDec ███████████ $612   Mar ████████ $448\nJan █████ $290        Apr ████████████ $655\nFeb █████ $301        May █████ $287\n```\n\n🏋️ Three holdings pay 58%: ENB (24%), BNS (19%), VDY (15%)\n⚠️ Cut risk: **ALA** payout ratio 112% of FCF, dividend held flat 3 yrs.',
      log=[('2.1.0','2026-11-01','Payout-ratio cut risk now uses free cash flow where available.'),('2.0.0','2026-10-12','Monthly bar chart, yield on cost, "how much do I need" calculator.'),('1.2.0','2026-09-20','DRIP-aware: counts reinvested shares.'),('1.0.0','2026-08-18','First release.')],
      reviews=[('maxstocks',5,'The monthly view is exactly how I think about it. Worth the $5.'),('northofthe49',5,'Called the ALA cut risk two weeks before the cut.'),('satoshi_sam',4,'Would love USD/CAD split.')],
      skill=md('''
---
name: dividend-income-planner
description: Projects the next 12 months of dividend income from the user's Blossom portfolio month by month, flags dividend-cut risk, and answers "how much do I need in X to earn Y per month". Use for any dividend income, yield, payout or DRIP question.
---

# Dividend Income Planner

## Needs
- Blossom Connector MCP: `get_holdings`, `get_dividends`
- Optional: Fiscal.ai MCP (payout ratios from free cash flow)

## Steps
1. `get_holdings` for every account. Keep dividend payers.
2. `get_dividends` for the next 12 months. Where a payer has no declared dividend yet, roll the last four payments forward and mark them "est.".
3. Build a month-by-month total. Render it as a two-column bar chart in a code block (one █ per $50, label the month and the $).
4. Yield on cost = projected 12-month income ÷ total cost basis.
5. Concentration: name the holdings that pay the top 50–60% of income.
6. Cut risk: payout ratio > 100% of free cash flow (Fiscal.ai) or > 90% of earnings, dividend flat for 3+ years, or a cut in the last 5 years. Flag with ⚠️ and one reason each.
7. If the user asks "how much do I need in X to earn Y", use X's trailing 12-month dividend per share and its current price; show the math.

## Rules
- Currency: show CAD and USD separately when both are present, then a CAD total at the current rate (say the rate).
- Never recommend a stock. Describe the portfolio the user has.
'''),
 ),
 dict(id='tfsa-rrsp-optimizer', shots=[('tfsa_1.jpg', 'Which account each holding belongs in, with the $ reason')], highlights=['Which account each holding belongs in, with the $ reason', "Foreign withholding-tax drag you're paying by accident", 'Contribution room left this year, from your Beevis profile', 'TFSA, RRSP, FHSA and non-registered covered'], emoji='🍁', name='TFSA & RRSP Room Optimizer', creator='tfsa_tina', cat='Canada',
      pitch='Which account each holding belongs in, how much room you have left this year, and the withholding tax you’re paying by accident.',
      downloads=3960, rating=4.7, ratings=191, updated='2026-10-29', version='1.2.0', requires=['blossom-connector'],
      price=dict(once=29), cadence='Each January (new limits) and after federal budgets',
      prompts=['Optimize my TFSA and RRSP', 'Am I holding US dividend stocks in the wrong account?', 'How much TFSA room do I have left for 2026?'],
      sample='**🍁 Account placement check**\n\n✅ 14 holdings are in the right account.\n⚠️ **3 moves worth making**\n\n| Holding | Now | Better | Why |\n|---|---|---|---|\n| SCHD | TFSA | RRSP | 15% US withholding tax on $1,140/yr of dividends isn’t recoverable in a TFSA |\n| XEQT | RRSP | TFSA | No foreign withholding drag; frees RRSP room for US payers |\n| CASH.TO | Non-reg | TFSA | Interest taxed at your marginal rate |\n\n**Room left in 2026:** TFSA $2,400 · RRSP $11,850 (from your Beevis survey — update it if you’ve contributed).',
      log=[('1.2.0','2026-10-29','FHSA added. Withholding-tax drag shown in dollars.'),('1.1.0','2026-10-02','Reads contribution room from the Beevis profile survey.'),('1.0.0','2026-09-10','First release.')],
      reviews=[('maxstocks',5,'Moved SCHD to my RRSP the same day. Paid for itself.'),('quantqueen',4,'Clear. Would like the US-listed vs Canadian-listed ETF comparison for the same index.')],
      skill=md('''
---
name: tfsa-rrsp-optimizer
description: Checks which registered account (TFSA, RRSP, FHSA, non-registered) each holding in a Canadian investor's Blossom portfolio should sit in, estimates foreign withholding-tax drag, and tracks contribution room. Use for TFSA, RRSP, FHSA, account placement or withholding tax questions.
---

# TFSA & RRSP Room Optimizer

## Needs
- Blossom Connector MCP: `get_holdings` (account type per position), `get_dividends`, `get_profile` (contribution room from the survey, if the user filled it in)

## Placement rules (apply in order)
1. US-listed stocks and ETFs paying dividends → RRSP first (treaty: no 15% withholding). In a TFSA the withholding is lost; in non-registered it is a foreign tax credit.
2. Canadian-listed ETFs holding US stocks (e.g. XEQT, VFV) → TFSA or RRSP; the withholding is inside the fund either way, so prefer TFSA to save RRSP room.
3. Interest-paying holdings (HISA ETFs, bonds, GICs) → TFSA/RRSP before non-registered; interest is fully taxable.
4. Canadian dividend payers → non-registered is acceptable (dividend tax credit); registered if room remains.
5. Highest expected growth → TFSA (withdrawals are tax-free).

## Steps
1. `get_holdings`. Group by account type.
2. For each holding, decide the better account from the rules; keep only changes that save ≥ $50/yr in tax drag or withholding (use `get_dividends` for the dollar amount).
3. Room: from `get_profile` if present; otherwise ask the user for this year's TFSA and RRSP room and say where to find it (CRA My Account).
4. Output: a ✅ count, then a table of moves (Holding, Now, Better, Why with the $ figure), then room left.

## Rules
- Describe tax treatment in general terms; the user's situation may differ, say so once.
- Never tell the user to sell; placement changes are theirs to make.
'''),
 ),
 dict(id='what-are-my-follows-buying', highlights=['What the people you follow bought and sold this week', 'Grouped by ticker, with the posts explaining why', 'Flips: first net-buying week in N', "Your weight vs your follows' average weight"], emoji='🐝', name='What are investors I follow buying?', creator='blossom', cat='Social',
      pitch='A weekly digest of what the investors you follow actually bought and sold, grouped by ticker, with the posts where they explained why.',
      downloads=12400, rating=4.9, ratings=802, updated='2026-11-05', version='1.6.0', requires=['blossom-connector','blossom-trade-data'],
      price=dict(free=True), cadence='Weekly',
      prompts=['What did the investors I follow buy this week?', 'Is anyone I follow selling NVDA?', 'Who I follow bought the dip on Thursday?'],
      sample='**🐝 This week, 23 of the 61 investors you follow traded**\n\n**Most bought** · NVDA (7 people, net +$41K) · SHOP (5) · VFV (4)\n**Most sold** · APP (6 people, net −$88K — @quantqueen: *"taking the +31% and walking"*) · TSLA (3)\n\n🔥 First time in 7 weeks that the people you follow were net buyers of SHOP. 3 of them posted why → [posts]\n\n👀 You hold NVDA at 6.2%. Your follows’ average weight is 9.8%.',
      log=[('1.6.0','2026-11-05','Links the posts where a follow explained a trade.'),('1.5.0','2026-10-22','"You hold X, your follows average Y" comparison line.'),('1.0.0','2026-09-01','First release.')],
      reviews=[('earningsedge',5,'This is the Blossom feed, but for trades.'),('tfsa_tina',5,'Replaced my Sunday scroll.'),('rebalancer_rob',5,'Love that it only shows what people chose to share.')],
      skill=md('''
---
name: what-are-my-follows-buying
description: Weekly digest of what the investors the user follows on Blossom bought and sold, grouped by ticker, with the posts explaining why and a comparison to the user's own position. Use when the user asks what people they follow are buying/selling, or for a weekly social trading digest.
---

# What are investors I follow buying?

## Needs
- Blossom Connector MCP: `get_following_activity`, `get_portfolio`
- Blossom Aggregate Trade Data MCP: `crowd_flows` (for the "vs everyone" line)

## Steps
1. `get_following_activity` for the last 7 days (or the range the user names). Only trades the investor chose to share are returned — say that once.
2. Group by ticker: people buying, people selling, net $ shared, and quote one explanation post per ticker if there is one (link it).
3. Rank: Most bought (by people, then $), Most sold.
4. Signals: a ticker where follows flipped from net selling to net buying (or back) after 4+ weeks; a ticker 3+ follows bought on the same day.
5. If the user holds any of the top tickers (`get_portfolio`), add "You hold X at a%, your follows average b%".
6. Close with the crowd line from `crowd_flows`: "All Blossom investors: net bought/sold X this week."

## Output
Headline line with counts, Most bought / Most sold, up to two 🔥 signals, the 👀 comparison line, the crowd line. Keep it under 150 words.
'''),
 ),
 dict(id='crowd-flow-scanner', shots=[('crowd_1.jpg', 'This week’s unusual tickers vs their own 12-week history'), ('crowd_2.jpg', '12 weeks of crowd flow for one ticker, with first-time buyers')], highlights=['Every ticker vs its own 12-week history', 'Volume ×, headcount ×, buy-share swings, net-flow flips', 'First-time-buyer and dormant-seller shares', 'Filters symbol remaps and take-privates'], emoji='📈', name='Crowd Flow Scanner', creator='blossom', cat='Screens',
      pitch='The spike detector behind the Blossom share cards: every ticker vs its own 12-week history — volume, people, flips, first-time buyers.',
      downloads=2870, rating=4.6, ratings=133, updated='2026-11-06', version='1.1.0', requires=['blossom-trade-data'],
      price=dict(monthly=9.99, yearly=79), cadence='Weekly, Monday before the open',
      prompts=['Scan for unusual trading on Blossom this week', 'Why is everyone selling AppLovin?', 'Which tickers flipped from net selling to net buying?'],
      sample='**📈 Unusual this week (vs each ticker’s 12-week history)**\n\n1. **APP** · $ traded 23× usual · 21% buys (62% usual) · net **−$1.7M** · stock +31% Thu → investors sold the rip\n2. **SHOP** · flipped to net buying after 7 weeks of selling · 38% of buyers are first-time holders\n3. **MRNA** · 130× volume · 44% of selling from accounts with no trades since 2023\n\n🚫 Filtered: INO, PARA, CHSN (symbol remaps, not sentiment).',
      log=[('1.1.0','2026-11-06','Symbol-remap filter. Dormant-seller share.'),('1.0.0','2026-10-27','First release, from the share-cards scanner.')],
      reviews=[('quantqueen',5,'The dormant-seller stat is something I can’t get anywhere else.'),('satoshi_sam',4,'Want crypto ETFs in scope.'),('northofthe49',4,'Good. Pricey for a weekly.')],
      skill=md('''
---
name: crowd-flow-scanner
description: Finds tickers trading unusually among Blossom investors versus their own 12-week history (volume multiple, headcount, buy-share swings, net-flow flips, first-time-buyer and dormant-seller shares) and explains the likely story. Use for "what's unusual", "why is everyone buying/selling X", or a weekly crowd scan.
---

# Crowd Flow Scanner

## Needs
- Blossom Aggregate Trade Data MCP: `anomalies`, `ticker_history`, `crowd_flows`

## Steps
1. `anomalies` for the week (or day). It returns volume ×, people ×, buy share vs usual, net-flow flips, first-time-buyer share and dormant-seller share for every ticker.
2. Drop mechanical stories: symbol remaps and relistings (volume × > 100 with mostly first-time traders and no news), take-privates, single-account positions. List what you dropped in one line.
3. Rank the rest by a simple score: volume × + 10 × |buy share − usual| + flip bonus.
4. For the top 5, `ticker_history` and one web search for the news. Write one line each: the numbers, then "→" and the story in plain words.
5. Never present a price move as a prediction. Describe what investors did.

## Output
Numbered list, one line per ticker, bold ticker, then the filtered line. Under 120 words.
'''),
 ),
 dict(id='portfolio-roast', highlights=['Your three worst habits, each with the exact number', 'Churn, hold time, cash drag, concentration, fee drag', 'Three fixes about behaviour, not stock picks', "Coach mode if you'd rather be gentle with yourself"], emoji='🔥', name='Portfolio Roast', creator='beevis', cat='Portfolio',
      pitch='Beevis in roast mode. Your portfolio’s three worst habits, with receipts, then three things to fix. Funnier than it should be.',
      downloads=15800, rating=4.7, ratings=1204, updated='2026-10-30', version='3.0.0', requires=['blossom-connector'],
      price=dict(free=True), cadence='Whenever Beevis learns a new insult',
      prompts=['Roast my portfolio', 'Be honest about my holdings', 'What would a hedge fund manager say about my TFSA?'],
      sample='🐝 **Oh, you’re *diversified*. 41% in three stocks that all rhyme with "AI".**\n\n1. 🫠 You bought TSLA 11 times and sold it 9 times. Net gain: $218. Time spent: a weekend.\n2. 🎢 Your "long-term" holding ENB has a 6-day average hold. \n3. 🏦 $14,300 in CASH.TO, in a non-registered account, paying tax on interest at 43%.\n\n**Three fixes:** stop trading TSLA · move CASH.TO into the TFSA · cap any single theme at 25%.',
      log=[('3.0.0','2026-10-30','New roast corpus. Fixes section is now mandatory.'),('2.2.0','2026-10-08','Hold-time and churn stats.'),('1.0.0','2026-07-15','First release.')],
      reviews=[('dividendsdan',5,'Hurt my feelings. Correct.'),('maxstocks',5,'The TSLA line got me.'),('earningsedge',4,'More coach, less roast, please. (It has a coach mode, I’m just soft.)')],
      skill=md('''
---
name: portfolio-roast
description: Beevis roast mode — reviews the user's Blossom portfolio and trade history, names the three worst habits with specific numbers, then gives three concrete fixes. Use when the user asks to roast, critique or be honest about their portfolio.
---

# Portfolio Roast

Voice: Beevis. Warm, blunt, funny, never cruel. One 🐝 at the start. Every joke has a number behind it.

## Needs
- Blossom Connector MCP: `get_portfolio`, `get_trades` (12 months), `get_holdings`

## Find the habits (pick the worst three)
- Concentration: top 3 weights, or one theme > 35%.
- Churn: a ticker bought and sold ≥ 5 times in 12 months; net P&L vs time.
- Hold time: average days held < 30 for something the user calls long-term (check post history if available).
- Cash drag: > 10% in cash-like holdings outside a registered account.
- Dividend chasing: yield > 9% positions with a recent cut.
- Fee drag: funds with MER > 1% when a cheaper twin exists.

## Output
1. One-line opener that lands the biggest habit.
2. Three numbered roasts, each with the exact figure from the tools.
3. "Three fixes:" one short clause each, specific to this portfolio.
No stock picks. Fixes are about behaviour and structure, not what to buy.
'''),
 ),
 dict(id='canadian-bank-earnings-prep', optional=['questrade-mcp'], highlights=['Reporting dates and the one thing to watch per bank', 'Dividend-raise odds from the last 8 quarters', 'PCL trend per bank', 'How Blossom investors are positioned going in'], emoji='🏦', name='Canadian Bank Earnings Prep', creator='northofthe49', cat='Earnings',
      pitch='Big Six earnings week, one page: what to watch per bank, PCL trends, dividend-raise odds, and how Blossom investors are positioned going in.',
      downloads=1760, rating=4.8, ratings=74, updated='2026-11-02', version='1.3.0', requires=['blossom-trade-data'],
      price=dict(monthly=2.99), cadence='Quarterly, the week before bank earnings',
      prompts=['Prep me for Canadian bank earnings', 'Will RY raise its dividend this quarter?', 'How are Blossom investors positioned in BNS before earnings?'],
      sample='**🏦 Bank week · Nov 25–28**\n\n| Bank | Reports | Watch | Div raise odds | Investors going in |\n|---|---|---|---|---|\n| RY | Wed | Wealth margins, City National | High (raises on Q4 pattern) | Net buyers 4 wks |\n| TD | Thu | AML remediation costs, US growth cap | Low | Net sellers, 31% buys |\n| BNS | Tue | International exit progress | Medium | **Net buyers, 1st time in 9 wks** |',
      log=[('1.3.0','2026-11-02','Dividend-raise odds from the last 8 quarters’ pattern.'),('1.2.0','2026-09-01','PCL trend column.'),('1.0.0','2026-05-20','First release.')],
      reviews=[('maxstocks',5,'Exactly what I want the Sunday before bank week.'),('tfsa_tina',5,'The positioning column is gold.')],
      skill=md('''
---
name: canadian-bank-earnings-prep
description: One-page preparation for Canadian Big Six bank earnings week — what to watch per bank, provisions for credit losses trend, dividend-raise likelihood from historical pattern, and how Blossom investors are positioned going in. Use before RY, TD, BNS, BMO, CM, NA earnings.
---

# Canadian Bank Earnings Prep

## Needs
- Blossom Aggregate Trade Data MCP: `crowd_flows`, `ticker_history`
- Optional: Fiscal.ai MCP for PCL history and consensus

## Steps
1. Find the reporting dates for RY, TD, BNS, BMO, CM, NA (web search; label as announced or estimated).
2. For each bank, one "watch" item from the last quarter's call and recent news (web search; one phrase, no speculation).
3. Dividend-raise odds: look at which quarters each bank raised in the last 8; if the bank raised in this quarter in ≥ 3 of the last 4 years, "High"; 1–2, "Medium"; 0, "Low". Show the pattern if asked.
4. Positioning: `ticker_history` for 4 weeks; summarise as net buyers/sellers and buy share; flag a flip.
5. Output the table, then two lines: the bank Blossom investors are most crowded into, and the one they have been leaving.
'''),
 ),
 dict(id='risk-concentration-check', shots=[('risk_1.jpg', 'Look-through sector mix and single-name exposure')], highlights=['Look-through: how much NVDA you own via your ETFs', 'Theme stacking and the combined “one bet”', '2022-style drawdown estimate in dollars', 'The smallest trims that reduce the biggest theme'], emoji='🛡️', name='Risk & Concentration Check', creator='quantqueen', cat='Portfolio',
      pitch='How much of your portfolio is one bet in disguise. Overlap across ETFs, theme exposure, a 2022-style drawdown estimate, and what to trim.',
      downloads=2310, rating=4.6, ratings=118, updated='2026-10-25', version='1.5.0', requires=['blossom-connector'],
      price=dict(yearly=19), cadence='Monthly',
      prompts=['Check my concentration risk', 'How much NVDA do I really own across my ETFs?', 'What would a 2022 do to my portfolio?'],
      sample='**🛡️ Look-through exposure**\n\nYou think you own NVDA at 6.2%. Through VFV, XEQT and QQC you own **11.9%**.\n\n**Theme stack:** AI chips & semis 24% · Big Tech 31% · overlap between them 14% → one bet ≈ **41%**\n\n📉 A 2022-style year (−33% on this mix) ≈ **−$38,700** on today’s value.\n\n✂️ Trimming QQC to 5% takes the AI stack to 18%.',
      log=[('1.5.0','2026-10-25','ETF look-through for 40 Canadian and US ETFs.'),('1.3.0','2026-09-14','2022-style drawdown estimate.'),('1.0.0','2026-08-01','First release.')],
      reviews=[('rebalancer_rob',5,'The look-through table is something every ETF investor needs to see once.'),('satoshi_sam',4,'Crypto ETFs not covered yet.')],
      skill=md('''
---
name: risk-concentration-check
description: Measures true concentration in the user's Blossom portfolio — look-through exposure across ETFs, theme stacking, correlated bets, a 2022-style drawdown estimate, and the smallest trims that reduce it. Use for risk, concentration, overlap or "how much X do I really own" questions.
---

# Risk & Concentration Check

## Needs
- Blossom Connector MCP: `get_portfolio`, `get_holdings`
- ETF holdings: use your knowledge of major ETF top-10 constituents (VFV, XEQT, VEQT, QQC, XIU, ZSP, SPY, QQQ, VTI…). Say "approximate" and the as-of quarter.

## Steps
1. `get_portfolio`. Separate single stocks from ETFs.
2. For each ETF, allocate its weight to its top-10 constituents (approximate) and a remainder.
3. Look-through table: for every stock the user holds directly, direct weight vs look-through weight.
4. Themes: map holdings to themes (AI chips & semis, Big Tech, Canadian banks, Energy, Crypto…). Sum theme weights; note overlap between related themes and the combined "one bet".
5. Drawdown: apply 2022 full-year returns by theme (approximate: US large growth −33%, Canadian banks −12%, energy +40%, bonds −12%, crypto −65%) to today's value. Label it an estimate.
6. Trims: the one or two position changes that most reduce the biggest theme, in the user's own holdings.

## Output
Look-through line, theme stack line, 📉 drawdown line, ✂️ trims. No recommendations beyond trims of what the user already holds.
'''),
 ),
 dict(id='fundamentals-deep-dive', optional=['public-mcp'], highlights=['Growth, margins, cash conversion, balance sheet', 'Two quarters of margin trend in bps', '“What changed” from the latest filing vs the prior one', 'What Blossom investors are doing with it'], emoji='🔎', name='Fundamentals Deep Dive', creator='earningsedge', cat='Research',
      pitch='A one-page tear sheet for any ticker from the filings: growth, margins, cash conversion, balance sheet, what changed this quarter, and what Blossom investors are doing with it.',
      downloads=1420, rating=4.8, ratings=61, updated='2026-10-31', version='1.1.0', requires=['fiscal-ai','blossom-trade-data'],
      price=dict(monthly=7.99, yearly=69), cadence='After each earnings season (template updates)',
      prompts=['Deep dive on SHOP', 'Did Constellation’s margins improve this quarter?', 'Tear sheet for CNQ'],
      sample='**🔎 SHOP · Q3 2026 tear sheet**\n\nRevenue $2.84B (+24% y/y) · GMV +26% · FCF margin 18% (16% last yr)\nGross margin 49.8% ▼ 110 bps (payments mix)\nNet cash $3.1B · no debt\n\n**What changed:** operating expenses grew faster than revenue for the first time in 6 quarters (AI hiring).\n**Blossom investors:** net buyers this week for the first time in 7 — 38% first-time holders.',
      log=[('1.1.0','2026-10-31','"What changed" section from the latest filing vs the prior one.'),('1.0.0','2026-10-05','First release.')],
      reviews=[('maxstocks',5,'This plus the Connector is my whole research stack now.'),('quantqueen',5,'Correct numbers, properly sourced. Rare.')],
      skill=md('''
---
name: fundamentals-deep-dive
description: Builds a one-page fundamentals tear sheet for a ticker from financial statements — growth, margins, cash conversion, balance sheet, what changed in the latest quarter — plus what Blossom investors are doing with it. Use for "deep dive", "tear sheet", "how are X's fundamentals" questions.
---

# Fundamentals Deep Dive

## Needs
- Fiscal.ai MCP: financial statements, ratios, estimates, filings
- Blossom Aggregate Trade Data MCP: `ticker_history`

## Steps
1. Latest quarter and the same quarter last year: revenue, growth, gross margin, operating margin, free cash flow and FCF margin, net cash or net debt. Show the y/y change for each.
2. Two quarters of trend for margins (▲/▼ with bps).
3. "What changed": compare the latest filing's MD&A themes to the prior quarter's; one or two sentences, sourced to the filing.
4. Estimates: next quarter consensus if available.
5. Blossom investors: `ticker_history` for 4 weeks; one line.

## Output
Headline with period, three stat lines, What changed, Blossom investors. Every number from a tool; cite the filing date. No price targets.
'''),
 ),
 dict(id='weekly-buzz-briefing', highlights=["This week's stories ranked by exposure to your holdings", 'Names the holdings and weights each story touches', 'What investors you follow did about it', 'Under 90 seconds, in the Weekly Buzz voice'], emoji='📰', name='Weekly Buzz Briefing', creator='blossom', cat='News',
      pitch='The Weekly Buzz, personalised: this week’s stories ranked by how much they touch your actual holdings, in 90 seconds.',
      downloads=9870, rating=4.8, ratings=512, updated='2026-11-07', version='1.8.0', requires=['blossom-connector'],
      price=dict(free=True), cadence='Weekly, Friday',
      prompts=['Give me my Weekly Buzz', 'What happened this week that affects my portfolio?', 'Catch me up on the market'],
      sample='**📰 Your Buzz · week of Nov 2**\n\n1. 🤖 **AppLovin +31% on earnings** — you don’t hold it, but 14% of your portfolio is in the AI-infra theme that rallied with it.\n2. 🍁 **BoC holds at 2.25%** — your 3 bank holdings (28% of portfolio) were flat; investors net bought BNS for the first time in 9 weeks.\n3. 🛍️ **Shopify −9% on the miss** — you hold 8.1%. Investors you follow bought the dip (5 of them).\n\n*3 more stories that don’t touch your holdings →*',
      log=[('1.8.0','2026-11-07','Ranks stories by exposure to your holdings and themes.'),('1.5.0','2026-10-10','Follows’ reaction line per story.'),('1.0.0','2026-08-22','First release.')],
      reviews=[('tfsa_tina',5,'The ranking by my holdings is the whole point.'),('dividendsdan',4,'Would like a dividend-news filter.')],
      skill=md('''
---
name: weekly-buzz-briefing
description: Personalised weekly market briefing in the Weekly Buzz voice — this week's top stories ranked by how much they affect the user's Blossom holdings and themes, with how investors reacted. Use for "catch me up", "what happened this week", "my weekly buzz".
---

# Weekly Buzz Briefing

Voice: the Weekly Buzz — conversational, emoji-led headlines, concrete numbers, Canadian-aware.

## Needs
- Blossom Connector MCP: `get_portfolio`, `get_following_activity`
- Web search for the week's stories

## Steps
1. `get_portfolio`; map holdings to themes.
2. Web search the week's 8–10 biggest market stories (indices, rates, big movers, Canada-specific).
3. Score each story by exposure: direct holding weight + 0.5 × theme weight. Rank.
4. For the top 3–5, write one headline with the number, one line on why it touches this portfolio (name the holdings and weights), and one line on what investors did (`get_following_activity` if any follows traded it).
5. End with "N more stories that don't touch your holdings →".

Under 180 words. No predictions.
'''),
 ),
 dict(id='crypto-allocation-guardrails', highlights=['Crypto share vs your target, in points and dollars', 'Counts coins and spot ETFs (IBIT, BTCC…)', 'Backtests rebalancing at the last three drifts', 'No view on where crypto is going'], emoji='🪙', name='Crypto Allocation Guardrails', creator='satoshi_sam', cat='Crypto',
      pitch='Keeps crypto at the share of your portfolio you decided on, tells you when it drifts, and shows what rebalancing would have done the last 3 times.',
      downloads=1180, rating=4.5, ratings=52, updated='2026-10-20', version='1.0.2', requires=['blossom-connector'],
      price=dict(yearly=14.99), cadence='Monthly',
      prompts=['Check my crypto allocation', 'Has my BTC drifted above my 5% target?', 'What if I had rebalanced crypto each quarter?'],
      sample='**🪙 Target 5% · now 9.3%** (BTC ran +48% since your last rebalance)\n\n⚠️ 4.3 pts over target. Trimming to 5% = $3,920.\n\n**Last 3 drifts:** rebalancing at 8%+ would have lifted total return by 1.9 pts and cut the max drawdown from −22% to −15%.',
      log=[('1.0.2','2026-10-20','Spot ETFs (IBIT, BTCC) counted as crypto.'),('1.0.0','2026-09-15','First release.')],
      reviews=[('quantqueen',5,'The drift history is a nice touch.'),('rebalancer_rob',4,'Works. Wish it covered the whole portfolio, not just crypto.')],
      skill=md('''
---
name: crypto-allocation-guardrails
description: Tracks the crypto share of the user's Blossom portfolio against their chosen target, flags drift, and backtests what rebalancing at past drifts would have done. Use for crypto allocation, BTC/ETH weight, or crypto rebalancing questions.
---

# Crypto Allocation Guardrails

## Needs
- Blossom Connector MCP: `get_holdings`, `get_trades`, `get_profile` (target from the survey if set)

## Steps
1. Identify crypto exposure: coins, spot ETFs (IBIT, FBTC, BTCC, ETHX…), and miners if the user wants them counted (ask once).
2. Current share vs target (ask for the target if the profile has none; suggest they save it).
3. Drift: over/under in points and dollars to trim or add.
4. History: from `get_trades` and price history, find the last 3 times the share exceeded target by 3+ points; estimate the return and max drawdown with vs without rebalancing to target. Label as an estimate.
5. Output: headline, ⚠️ drift line, history line. No view on crypto's direction.
'''),
 ),
 dict(id='rebalance-planner', shots=[('rebalance_1.jpg', 'Target vs reality, and the fix using new contributions only')], highlights=['Target mix vs reality, by account', 'Uses new contributions first so you sell less', 'Registered accounts first: no tax events', 'Trade table with account, action, amount'], emoji='🎯', name='Rebalance Planner', creator='rebalancer_rob', cat='Portfolio',
      pitch='Your target mix vs reality, and the fewest trades (in the right accounts) to get back to it — with new contributions used first so you sell less.',
      downloads=2050, rating=4.7, ratings=97, updated='2026-11-01', version='2.0.0', requires=['blossom-connector'],
      price=dict(monthly=4.99, yearly=39), cadence='Monthly, and after any 5-point drift',
      prompts=['Plan my rebalance', 'I have $2,000 to add — where does it go?', 'Am I still 80/20?'],
      sample='**🎯 Target 70/20/10 (equity / bonds / cash) · now 76/16/8**\n\nWith your **$2,000** contribution, 3 buys and 0 sells get you to 71/20/9:\n\n| Account | Action | Amount |\n|---|---|---|\n| TFSA | Buy XBB | $1,200 |\n| RRSP | Buy VAB | $500 |\n| TFSA | Buy CASH.TO | $300 |\n\nNo sells needed → no tax events. Next check: Dec 1.',
      log=[('2.0.0','2026-11-01','Contribution-first rebalancing; account-aware (registered first).'),('1.4.0','2026-10-03','Drift alert threshold is configurable.'),('1.0.0','2026-08-05','First release.')],
      reviews=[('tfsa_tina',5,'Account-aware rebalancing is the feature. Nobody else does it.'),('maxstocks',4,'Great. Wants a Blossom post template for the result.')],
      skill=md('''
---
name: rebalance-planner
description: Compares the user's Blossom portfolio to their target allocation and produces the fewest trades, in the right accounts, to return to target — using new contributions before any sells. Use for rebalancing, "where should this contribution go", or allocation drift questions.
---

# Rebalance Planner

## Needs
- Blossom Connector MCP: `get_holdings` (by account), `get_profile` (target mix if saved)

## Steps
1. Target: from the profile, or ask (equity / bonds / cash, and any sub-targets like Canada/US/International).
2. Current mix from `get_holdings`, classifying each holding (ETF lookups as approximate).
3. If the user names a contribution, allocate it to the most-underweight buckets first; compute the resulting mix.
4. Only if still > 3 points off target, propose sells — registered accounts first (no tax), then non-registered with the smallest gains.
5. Output: target vs now, the trade table (Account, Action, Amount), tax note, next check date.

Never suggest a specific new ticker; rebalance with what the user already holds unless a bucket is empty, then name the broad-index ETF type and let them choose.
'''),
 ),
]
