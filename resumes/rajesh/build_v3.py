"""Rajesh K M - cloud-platform positioning, with and without the Lycatel role.

Reuses the design system from build_v2.py. BPO wording is removed from the
headline, stats, summary and competencies (the employer name "Lycatel BPO" is kept
verbatim where that role appears). Facts (employers, titles, dates, education,
metrics) are unchanged; no certifications, tools or numbers were added.

Usage: python3 build_v3.py OUT_DIR
"""
import sys, pathlib
sys.argv = [sys.argv[0]] + sys.argv[1:]
import build_v2 as v2
from build_v2 import b, ul, ICON, PHOTO, CSS
from playwright.sync_api import sync_playwright

OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
EXTRA = """
.step.early{background:#f4f6f9;border-left-color:#aab3c8}.step.early b{color:#4a5472;font-weight:700}
.step.early span,.step.early em{color:#7b849f}
.step.solo{flex:none;width:49%}
.early-wrap{margin-top:2.4mm;border:.3mm dashed #b9c1d4;border-radius:1.4mm;padding:2mm 3mm 1mm;background:#fafbfd;break-inside:avoid}
.early-head{display:flex;justify-content:space-between;align-items:baseline;font-size:8.8pt;color:#4a5472;margin-bottom:1.2mm}
.early-head b{letter-spacing:.04em}.early-head span{font-size:8pt;color:#7b849f}
.early-wrap li{font-size:8.5pt;color:#3b4258}
.early-wrap li:before{background:#aab3c8}
"""

def page1(v):
    stats = "".join(f'<div class="stat"><b>{n}</b><span>{l}</span></div>' for n, l in v["stats"])
    tl = ""
    for i, (t, org, yrs, tag, cls) in enumerate(v["timeline"]):
        tl += f'<div class="step {cls}"><b>{t}</b><span>{org}</span><span>{yrs}</span><em>{tag}</em></div>'
    chips = "".join(f'<span class="chip">{c}</span>' for c in v["competencies"])
    return f"""
<div class="page">
 <aside class="side">
  <div class="photo"><img src="{PHOTO}"></div>
  <section class="contact"><h3>Contact</h3>
   <div>{ICON['phone'].replace('<svg','<svg class="ico"')}<span>+91 99769 99981</span></div>
   <div>{ICON['mail'].replace('<svg','<svg class="ico"')}<span>kmrajesh05@yahoo.com</span></div>
   <div>{ICON['pin'].replace('<svg','<svg class="ico"')}<span>Chennai, India</span></div></section>
  <section class="edu"><h3>Education</h3>
   <div><b>MBA</b><span>Marketing &amp; Sales Management</span><span>NIBM</span><i>2018 – 2020</i></div>
   <div><b>PG Diploma in Project Management (PGDBA)</b><span>NIBM</span><i>2015 – 2016</i></div>
   <div><b>Bachelor of Business Administration</b><span>Annamalai University</span><i>2006 – 2009</i></div></section>
  <section><h3>Core Competencies</h3><div class="chips">{chips}</div></section>
 </aside>
 <main class="main">
  <header><div class="name">RAJESH K M</div><div class="role">{v['title']}</div><p class="tag">{v['tagline']}</p></header>
  <div class="stats">{stats}</div>
  <section><h2>Profile Summary</h2>{ul(v['summary'])}</section>
  <section><h2>Career Timeline</h2><div class="tl">{tl}</div></section>
  <section><h2>Work Experience</h2>
   <div class="job"><div class="jobhead"><b>MANAGER</b><span>Dec 2015 – Present</span></div>
   <div class="jobsub">BankBazaar <span>Chennai, India</span></div>
   <div class="kra">Key Result Areas</div>{ul(v['bankbazaar'])}</div></section>
 </main>
</div>"""

def page2(v):
    cards = "".join(f'<div class="card"><b>{t}</b><small>{o}</small><p>{d}</p><em>{r}</em></div>' for t, o, d, r in v["cards"])
    tech = "".join(f'<div class="tx"><b>{t}</b><p>{d}</p></div>' for t, d in v["tech"])
    strengths = "".join(f"<li>{s}</li>" for s in v["strengths"])
    domains = "".join(f'<span class="chip">{d}</span>' for d in v["domains"])
    early = ""
    if v.get("lycatel"):
        early = f"""<div class="early-wrap"><div class="early-head"><b>EARLY CAREER · SUPERVISOR</b><span>Lycatel BPO · Nov 2006 – Jun 2009</span></div>{ul(v['lycatel'])}</div>"""
    return f"""
<div class="page">
 <aside class="side">
  <section><h3>Technical Exposure</h3>{tech}</section>
  <section><h3>Key Strengths</h3><ul>{strengths}</ul></section>
  <section><h3>Domain Expertise</h3><div class="chips">{domains}</div></section>
  <section><h3>Languages</h3><div class="chips"><span class="chip">English</span><span class="chip">Tamil</span><span class="chip">Telugu</span></div></section>
 </aside>
 <main class="main" style="padding-top:11mm">
  <section><h2>Work Experience (continued)</h2>
   <div class="job"><div class="jobhead"><b>TEAM LEADER</b><span>May 2010 – Sep 2015</span></div>
   <div class="jobsub">eNoah iSolution (P) Ltd <span>Chennai, India</span></div>
   <div class="kra">Key Result Areas</div>{ul(v['enoah'])}</div>
   {early}</section>
  <section><h2>Cloud &amp; Automation Initiatives</h2><div class="cards">{cards}</div></section>
 </main>
</div>"""

BB = [
 "Led cross-functional teams through the **migration of operations and customer data to cloud platforms**, achieving a **20% growth** in customer acquisition and retention within three years.",
 "Owned **cloud solution rollouts for telephony, CRM and reporting**, boosting operational efficiency by **15%** with significant cost reductions and faster service delivery.",
 "**Automated storage, retrieval and reporting** of customer and application data on cloud platforms, cutting manual handling and speeding up service delivery.",
 "Planned migrations end to end: requirement gathering, data mapping and validation, cut-over scheduling and post-go-live support, keeping a **30-member** credit card operation live throughout.",
 "Managed cloud vendors, negotiating contracts that **cut expenses by 10%** while upholding service quality and data security standards.",
 "Kept **data security and regulatory compliance** in place on hosted systems through every platform transition, working with IT, security and business stakeholders.",
 "Delivered **targeted training programs** so teams adopted cloud tools quickly, ensuring seamless operations and increased productivity.",
]
EN = [
 "Ran medical-information retrieval for a **USA dental insurance** client on **secure, cloud-hosted repositories**, organizing policy, certificate and renewal records for fast, accurate access and ensuring compliance.",
 "Implemented quality control and **data-security protocols on hosted systems**, maintaining regulatory compliance and boosting the efficiency of medical information retrieval for dental insurance claims.",
 "**Automated recurring storage, retrieval and verification steps** on hosted repositories to reduce manual effort and turnaround time for international clients.",
 "Worked with vendors and IT partners to migrate hosted platforms and resolve complex cases, **lifting client satisfaction by 20%** in line with industry regulations.",
 "Directed the **Walt Disney E-Publishing Project**, moving content publishing and proofreading workflows to shared online platforms for error-free output.",
 "Coordinated project timelines and cross-functional teams to deliver high-quality, brand-consistent content on schedule, upholding Disney’s standards for precision and publishing excellence.",
 "Guided team members through the move to hosted tools with coaching and clear quality standards, sustaining accuracy and productivity.",
]
LY = [
 "Led a team of 35 associates to consistently exceed KPIs for USA and UK telecom clients, supporting the shift from legacy systems to centralized, hosted telephony and web-based tools with uninterrupted service.",
 "Enhanced customer satisfaction scores by 15% and achieved 100% SLA compliance, with cross-functional work with IT and other departments driving a 10% increase in client retention.",
]
CARDS4 = [
 ("Cloud Migration of Credit Card Operations", "BankBazaar · Manager", "Moved operations and customer data to cloud platforms with planned cut-overs, data validation and post-go-live support.", "20% growth · 15% efficiency"),
 ("Cloud Storage &amp; Reporting Automation", "BankBazaar · Manager", "Automated storage, retrieval and reporting on cloud platforms to cut manual handling and speed up delivery.", "Faster service delivery"),
 ("Cloud Telephony, CRM &amp; Reporting Rollout", "BankBazaar · Manager", "Rolled out cloud solutions with IT and vendors, backed by user training for quick adoption.", "10% lower expenses"),
 ("Secure Cloud-Hosted Document Repositories", "eNoah · USA dental insurance", "Ran medical-information retrieval on secure hosted repositories with data-security and compliance protocols.", "20% client satisfaction"),
]
CARDS6 = CARDS4 + [
 ("Shared Online Publishing Platform", "eNoah · Walt Disney E-Publishing Project", "Moved content publishing and proofreading workflows onto shared online platforms for consistent, error-free output.", "Error-free output"),
 ("Security &amp; Compliance on Hosted Systems", "eNoah &amp; BankBazaar", "Applied data-security protocols and compliance checks across hosted systems handling regulated information.", "Regulatory compliance"),
]
TECH = [("Cloud Platforms &amp; Storage", "Cloud-hosted repositories, cloud telephony and CRM, cloud reporting dashboards"),
        ("Automation", "Automated storage, retrieval, verification and reporting workflows"),
        ("Migration &amp; Cut-over", "Migration planning, data mapping and validation, cut-over scheduling, post-go-live support"),
        ("Security &amp; Compliance", "Data-security protocols, access control, regulatory compliance on hosted systems"),
        ("Vendor &amp; Cost Management", "Cloud vendor selection, contract and licence negotiation, cost optimization")]
COMP = ["Cloud Migration Planning", "Cloud Storage Automation", "Cloud Platform Operations", "Workflow Automation", "Data Migration &amp; Validation", "Data Security &amp; Compliance", "Cut-over &amp; Release Management", "Cloud Vendor &amp; Cost Management", "Reporting &amp; Dashboards", "Project Management", "Stakeholder Management", "Team Leadership", "Training &amp; Adoption"]
STR = ["Calm, structured leader through platform transitions", "Hands-on team leadership: led a team of 30", "Security- and compliance-first mindset", "Multi-domain: banking, insurance &amp; publishing", "Quick learner with a tech-enabled problem-solving approach"]

WITH = dict(
 file="Rajesh_K_M_Resume_Cloud_Platform_With_Lycatel.pdf",
 title="Cloud Engineer | Cloud Migration, Storage &amp; Automation",
 tagline="Cloud engineer delivering cloud migrations, cloud storage and workflow automation, and secure hosted platforms for financial services and insurance clients, with a record of improving efficiency, cost and data security. Backed by 18 years of professional experience.",
 stats=[("18+", "Years of experience"), ("30", "Team members led"), ("20%", "Growth in acquisition &amp; retention"), ("15%", "Operational efficiency gain"), ("10%", "Lower vendor expenses")],
 timeline=[("Supervisor", "Lycatel BPO", "2006 – 2009", "Early career", "early"), ("Team Leader", "eNoah iSolution", "2010 – 2015", "Cloud-hosted repositories", ""), ("Manager", "BankBazaar", "2015 – Present", "Cloud migration", "now")],
 summary=[
  "**Cloud engineer** across financial services and insurance, taking cloud migration, storage and automation initiatives from planning to cut-over and support.",
  "Led migration of operations and customer data to **cloud platforms** while leading a **team of 30**, supporting a **20% growth** in customer acquisition and retention.",
  "Owned **cloud solution rollouts** for telephony, CRM and reporting, coordinating IT, vendors and users to keep service running without disruption.",
  "**Automated storage, retrieval and reporting workflows** on cloud-hosted repositories and dashboards, cutting manual effort and lifting efficiency by **15%**.",
  "Keeps **data security and regulatory compliance** in place on hosted systems handling regulated financial and insurance information.",
  "Manages **cloud vendors and costs**: contracts negotiated to **cut expenses by 10%** while upholding service quality and security standards.",
 ],
 competencies=COMP, bankbazaar=BB, enoah=EN, lycatel=LY, cards=CARDS6, cards_title="", tech=TECH, strengths=STR + ["International client delivery (USA &amp; UK)"],
 domains=["Banking &amp; Financial Services", "Credit Cards", "Insurance (USA Dental)", "E-Publishing (Walt Disney)"],
)

WITHOUT = dict(
 file="Rajesh_K_M_Resume_Cloud_Platform_Without_Lycatel.pdf",
 title="Cloud Engineer | Cloud Migration, Storage &amp; Automation",
 tagline="Cloud engineer delivering cloud migrations, cloud storage and workflow automation, and secure hosted platforms for financial services and insurance clients, with a record of improving efficiency, cost and data security. Backed by 18 years of professional experience.",
 stats=[("18+", "Years of experience"), ("30", "Team members led"), ("20%", "Growth in acquisition &amp; retention"), ("15%", "Operational efficiency gain"), ("10%", "Lower vendor expenses")],
 timeline=[("Team Leader", "eNoah iSolution", "2010 – 2015", "Cloud-hosted repositories", ""), ("Manager", "BankBazaar", "2015 – Present", "Cloud migration", "now")],
 summary=WITH["summary"],
 competencies=COMP, bankbazaar=BB, enoah=EN, lycatel=None, cards=CARDS6, cards_title="", tech=TECH, strengths=STR + ["Client delivery for international (USA) accounts"],
 domains=["Banking &amp; Financial Services", "Credit Cards", "Insurance (USA Dental)", "E-Publishing (Walt Disney)"],
)

def build(v):
    css = CSS + EXTRA + (".tl{gap:2mm}" if not v.get("lycatel") else "")
    doc = f"<!doctype html><html><head><meta charset='utf-8'><title>Rajesh K M - Resume</title><style>{css}</style></head><body>{page1(v)}{page2(v)}</body></html>"
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        pg = br.new_page(); pg.set_content(doc); pg.wait_for_timeout(300)
        over = pg.evaluate("""()=>[...document.querySelectorAll('.page')].map((p,i)=>{
          const m=p.querySelector('.main'), s=p.querySelector('.side');
          return {page:i+1, mainOver:m.scrollHeight-m.clientHeight, sideOver:s.scrollHeight-s.clientHeight}})""")
        print(v["file"], over)
        pg.pdf(path=str(OUT / v["file"]), format="A4", print_background=True, prefer_css_page_size=True)
        br.close()

if __name__ == "__main__":
    for v in (WITH, WITHOUT): build(v)
