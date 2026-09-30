"""Rajesh K M - enhanced 2-page resumes (Automation / Cloud variants).

Layout is inspired by a reference resume (sidebar + highlights + timeline + key
result areas). All facts (employers, titles, dates, education, metrics) come from
Rajesh's original resume; no certifications, tools or numbers were added.

Usage: python3 build_v2.py OUT_DIR
"""
import base64, html, sys, pathlib
from playwright.sync_api import sync_playwright

HERE = pathlib.Path(__file__).parent
OUT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".")
PHOTO = "data:image/jpeg;base64," + base64.b64encode((HERE / "photo_trimmed_mustache.jpg").read_bytes()).decode()

def b(s):  # **bold** -> <b>
    parts = html.escape(s).split("**")
    return "".join(f"<b>{p}</b>" if i % 2 else p for i, p in enumerate(parts))

def ul(items): return "<ul>" + "".join(f"<li>{b(i)}</li>" for i in items) + "</ul>"

ICON = {
 "phone": '<svg viewBox="0 0 24 24"><path d="M6.6 10.8a15 15 0 006.6 6.6l2.2-2.2a1 1 0 011-.25 11.4 11.4 0 003.6.6 1 1 0 011 1V20a1 1 0 01-1 1A17 17 0 013 4a1 1 0 011-1h3.5a1 1 0 011 1c0 1.25.2 2.45.6 3.6a1 1 0 01-.25 1z"/></svg>',
 "mail": '<svg viewBox="0 0 24 24"><path d="M3 5h18a1 1 0 011 1v12a1 1 0 01-1 1H3a1 1 0 01-1-1V6a1 1 0 011-1zm9 8L4.5 7.5v1.2L12 14l7.5-5.3V7.5z"/></svg>',
 "pin": '<svg viewBox="0 0 24 24"><path d="M12 2a7 7 0 00-7 7c0 5 7 13 7 13s7-8 7-13a7 7 0 00-7-7zm0 9.5A2.5 2.5 0 1112 6.5a2.5 2.5 0 010 5z"/></svg>',
}

CSS = """
@page{size:A4;margin:0}
*{box-sizing:border-box;margin:0;padding:0}
:root{--navy:#2b3247;--navy2:#3a4360;--accent:#1e88a8;--tint:#eef3f8;--ink:#1c2029;--mute:#5d6786}
body{font-family:'Liberation Sans',Arial,sans-serif;color:var(--ink);font-size:8.9pt;line-height:1.36}
.page{width:210mm;height:297mm;display:flex;position:relative;overflow:hidden;page-break-after:always;background:#fff}
.side{width:62mm;background:var(--navy);color:#e9edf6;padding:11mm 6.5mm 8mm;display:flex;flex-direction:column;gap:5.5mm}
.main{flex:1;padding:10mm 10mm 7mm 9mm;display:flex;flex-direction:column;gap:3.6mm}
.photo{width:36mm;height:36mm;border-radius:50%;border:1.2mm solid #fff;margin:0 auto 1mm;overflow:hidden;background:#ccd}
.photo img{width:100%;height:100%;object-fit:cover;object-position:50% 40%}
.side h3{font-size:9.6pt;letter-spacing:.14em;text-transform:uppercase;color:#fff;padding-bottom:1.6mm;border-bottom:.5mm solid var(--accent);margin-bottom:2.6mm}
.contact div{display:flex;gap:2.4mm;align-items:flex-start;margin-bottom:2mm;font-size:8.6pt;word-break:break-all}
.contact svg,.ico{width:4.2mm;height:4.2mm;flex:none;fill:#fff;background:var(--accent);border-radius:50%;padding:.9mm}
.edu div{margin-bottom:2.6mm}.edu b{color:#fff;display:block;font-size:8.7pt}
.edu span{display:block;color:#c3cadd;font-size:8.2pt}.edu i{color:#9fd8e8;font-size:8pt;font-style:normal}
.chips{display:flex;flex-wrap:wrap;gap:1.5mm}
.chip{font-size:7.9pt;background:var(--navy2);border:.25mm solid #56618a;border-radius:1.6mm;padding:.9mm 2mm;color:#fff}
.side ul{list-style:none}.side li{position:relative;padding-left:3.6mm;margin-bottom:1.7mm;font-size:8.5pt}
.side li:before{content:"";position:absolute;left:0;top:1.5mm;width:1.7mm;height:1.7mm;background:var(--accent);border-radius:50%}
.tx b{display:block;color:#fff;font-size:8.6pt;margin-bottom:.4mm}.tx p{color:#c3cadd;font-size:8.2pt;margin-bottom:2.4mm}
.name{font-size:29pt;font-weight:700;letter-spacing:.01em;line-height:1;color:var(--navy)}
.role{font-size:12pt;font-weight:700;color:var(--accent);margin-top:1.6mm}
.tag{margin-top:1.6mm;color:#3b4258;text-align:justify}
.stats{display:flex;background:var(--navy);border-radius:2mm;color:#fff;padding:2.3mm 1mm}
.stat{flex:1;text-align:center;border-right:.25mm solid #56618a;padding:0 1mm}.stat:last-child{border:0}
.stat b{display:block;font-size:14pt;color:#7fd3ea;line-height:1.1}.stat span{font-size:7.2pt;color:#dfe5f3;line-height:1.15;display:block}
h2{font-size:11pt;letter-spacing:.06em;text-transform:uppercase;color:var(--navy);border-bottom:.45mm solid var(--navy);padding-bottom:1mm;margin-bottom:2.2mm;display:flex;align-items:center;gap:2mm}
h2:before{content:"";width:2.6mm;height:4.2mm;background:var(--accent);border-radius:.6mm}
.main ul{list-style:none}.main li{position:relative;padding-left:4mm;margin-bottom:1.35mm;text-align:justify}
.main li:before{content:"";position:absolute;left:.7mm;top:1.55mm;width:1.6mm;height:1.6mm;background:var(--accent);border-radius:50%}
.tl{display:flex;gap:1mm;margin-top:.5mm}
.step{flex:1;background:var(--tint);border-left:1.2mm solid var(--accent);padding:1.7mm 2.4mm;border-radius:0 1.4mm 1.4mm 0}
.step.now{background:var(--navy);border-color:#7fd3ea;color:#fff}
.step b{display:block;font-size:9.4pt}.step span{display:block;font-size:8pt;color:var(--mute)}.step.now span{color:#cfe9f3}
.step em{display:block;font-style:normal;font-size:7.8pt;font-weight:700;color:var(--accent);margin-top:.4mm}.step.now em{color:#7fd3ea}
.job{break-inside:avoid;margin-bottom:1.2mm}
.jobhead{background:var(--navy);color:#fff;display:flex;justify-content:space-between;align-items:baseline;padding:1.5mm 3mm;border-radius:1.2mm 1.2mm 0 0}
.jobhead b{font-size:10.4pt;letter-spacing:.03em}.jobhead span{font-size:8.6pt;color:#cfe9f3}
.jobsub{background:var(--tint);padding:1.3mm 3mm;display:flex;justify-content:space-between;font-size:8.7pt;font-weight:700;color:var(--navy);border-radius:0 0 1.2mm 1.2mm;margin-bottom:1.6mm}
.jobsub span{color:var(--mute);font-weight:400}
.kra{font-weight:700;color:var(--accent);margin-bottom:1mm;font-size:8.8pt}
.cards{display:grid;grid-template-columns:1fr 1fr;gap:2.6mm}
.card{border:.3mm solid #cfd8e6;border-top:1mm solid var(--accent);border-radius:1.4mm;padding:2.2mm 2.8mm;background:#fff;break-inside:avoid}
.card b{display:block;font-size:9pt;color:var(--navy);line-height:1.25}.card small{display:block;color:var(--mute);font-size:7.7pt;margin:.3mm 0 1.2mm}
.card p{font-size:8.5pt;color:#2f3548;text-align:left}.card em{display:inline-block;margin-top:1.4mm;font-style:normal;font-size:7.8pt;font-weight:700;background:#dff2f8;color:#0f6a86;border-radius:1mm;padding:.5mm 1.8mm}
"""

def page1(v):
    stats = "".join(f'<div class="stat"><b>{n}</b><span>{l}</span></div>' for n, l in v["stats"])
    tl = ""
    for i, (t, org, yrs, tag) in enumerate(v["timeline"]):
        tl += f'<div class="step{" now" if i == 2 else ""}"><b>{t}</b><span>{org}</span><span>{yrs}</span><em>{tag}</em></div>'
    chips = "".join(f'<span class="chip">{c}</span>' for c in v["competencies"])
    bb = v["bankbazaar"]
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
   <div class="kra">Key Result Areas</div>{ul(bb)}</div></section>
 </main>
</div>"""

def page2(v):
    ten = ul(v["enoah"]); ly = ul(v["lycatel"])
    cards = "".join(f'<div class="card"><b>{t}</b><small>{o}</small><p>{d}</p><em>{r}</em></div>' for t, o, d, r in v["cards"])
    tech = "".join(f'<div class="tx"><b>{t}</b><p>{d}</p></div>' for t, d in v["tech"])
    strengths = "".join(f"<li>{s}</li>" for s in v["strengths"])
    return f"""
<div class="page">
 <aside class="side">
  <section><h3>Technical Exposure</h3>{tech}</section>
  <section><h3>Key Strengths</h3><ul>{strengths}</ul></section>
  <section><h3>Domain Expertise</h3><div class="chips"><span class="chip">Banking &amp; Financial Services</span><span class="chip">Credit Cards</span><span class="chip">Insurance (USA Dental)</span><span class="chip">Telecom (USA &amp; UK)</span><span class="chip">E-Publishing (Walt Disney)</span></div></section>
  <section><h3>Languages</h3><div class="chips"><span class="chip">English</span><span class="chip">Tamil</span><span class="chip">Telugu</span></div></section>
 </aside>
 <main class="main" style="padding-top:11mm">
  <section><h2>Work Experience (continued)</h2>
   <div class="job"><div class="jobhead"><b>TEAM LEADER</b><span>May 2010 – Sep 2015</span></div>
   <div class="jobsub">eNoah iSolution (P) Ltd <span>Chennai, India</span></div>
   <div class="kra">Key Result Areas</div>{ten}</div>
   <div class="job" style="margin-top:3mm"><div class="jobhead"><b>SUPERVISOR</b><span>Nov 2006 – Jun 2009</span></div>
   <div class="jobsub">Lycatel BPO <span>USA &amp; UK telecom accounts</span></div>
   <div class="kra">Key Result Areas</div>{ly}</div></section>
  <section><h2>{v['cards_title']}</h2><div class="cards">{cards}</div></section>
 </main>
</div>"""

COMMON_TL = lambda a, b_, c: [("Supervisor", "Lycatel BPO", "2006 – 2009", a), ("Team Leader", "eNoah iSolution", "2010 – 2015", b_), ("Manager", "BankBazaar", "2015 – Present", c)]
STRENGTHS_TAIL = ["Leadership at scale: teams of 150+", "Compliance-first, quality-driven mindset", "International client delivery (USA &amp; UK)", "Multi-domain: banking, insurance, telecom &amp; publishing", "Quick learner with a tech-enabled problem-solving approach"]

AUTOMATION = dict(
 file="Rajesh_K_M_Resume_Automation_Enhanced.pdf",
 title="Manager | BPO Operations &amp; Process Automation",
 tagline="Results-driven BPO operations leader with 18 years of experience across credit card, insurance and telecom services, known for replacing manual, repetitive work with automated workflows that improve speed, accuracy, compliance and client satisfaction.",
 stats=[("18+", "Years in BPO &amp; operations"), ("150+", "Team members led"), ("20%", "Growth in acquisition &amp; retention"), ("15%", "Operational efficiency gain"), ("100%", "SLA compliance")],
 timeline=COMMON_TL("35-member team · telecom", "USA dental insurance", "150+ team · automation"),
 summary=[
  "**Operations and automation leader** across credit card, dental insurance and telecom BPO accounts for USA, UK and Indian clients.",
  "Led a **high-performing team of 150+** in credit card operations, driving revenue growth by automating and optimizing the application submission process.",
  "Spots **manual, repetitive processes** and partners with IT and vendors to replace them with automation, macros, routing rules and real-time reporting dashboards.",
  "Designs **targeted training programs** that upskill employees across roles, so new tools and workflows are adopted quickly and productivity rises.",
  "Strong **decision-making under pressure**: swiftly identifies critical issues, escalates concerns and implements effective solutions.",
  "Consistent record of **SLA and regulatory compliance**, higher customer satisfaction (up to 20%) and better client retention (10%), with vendor contracts negotiated to **cut expenses by 10%**.",
 ],
 competencies=["Process Automation", "Workflow Optimization", "Operations Management", "Team Leadership", "SLA &amp; KPI Management", "Quality Control", "Regulatory Compliance", "Vendor Management", "Training &amp; Upskilling", "Stakeholder Management", "Project Coordination", "Client Retention", "Cost Optimization", "Process Improvement"],
 bankbazaar=[
  "Led cross-functional teams to **automate application submission and lead-processing workflows**, achieving a **20% growth** in customer acquisition and retention within three years.",
  "Replaced manual, repetitive processes with **automation, scripts and real-time dashboards**, boosting operational efficiency by **15%** with significant cost reductions and faster service delivery.",
  "Managed vendor and stakeholder relationships for automation tools and services, negotiating contracts that **cut expenses by 10%** while upholding superior service quality standards.",
  "Led and mentored a **team of 150+** in credit card operations, coaching team leaders and agents to adopt automated tools and new workflows.",
  "Delivered **targeted training programs** across roles, ensuring seamless operations and increased productivity during every process change.",
  "Tracked KPIs and turnaround times through automated reports, swiftly identifying critical issues, escalating concerns and implementing effective solutions.",
  "Partnered with IT, product and compliance teams to prioritize automation opportunities and roll out changes without disrupting service.",
 ],
 enoah=[
  "Led a specialized team in the **USA dental insurance sector**, managing medical retrieval through detailed analysis of policies, certificates and renewals, automating repetitive steps to ensure compliance and accuracy for international clients.",
  "Implemented quality control protocols with **automated verification checks**, maintaining regulatory compliance and boosting the efficiency of medical information retrieval essential for dental insurance claims.",
  "Worked with vendors to automate case hand-offs and resolve complex cases, streamlining service delivery and **increasing client satisfaction by 20%**, in line with industry regulations.",
  "Directed the **Walt Disney E-Publishing Project**, automating content publishing steps and proofreading checks to ensure error-free output.",
  "Coordinated project timelines and cross-functional teams to deliver high-quality, brand-consistent content on schedule, upholding Disney’s standards for precision and publishing excellence.",
  "Coached team members on process changes and quality standards, sustaining accuracy and productivity targets for international clients.",
 ],
 lycatel=[
  "Led a **team of 35 associates** to consistently exceed key performance indicators (KPIs) in internal customer service operations for USA and UK telecom clients.",
  "Introduced **macros, call-routing rules and automated reports** to cut manual effort, enhancing customer satisfaction scores by **15%** and surpassing client expectations for international accounts.",
  "Developed tailored strategies and automated tracking to meet unique client requirements, achieving **100% compliance** with service level agreements (SLAs) and regulatory standards.",
  "Collaborated cross-functionally to optimize and automate workflows, driving a **10% increase in client retention** and overall satisfaction.",
  "Monitored associate performance against KPIs and gave regular feedback, sustaining quality and productivity targets.",
 ],
 cards_title="Automation Initiatives",
 cards=[
  ("Credit Card Application Workflow Automation", "BankBazaar · Manager", "Streamlined the end-to-end application submission journey, removing manual touchpoints and rework across a 150+ member operation.", "20% growth · 15% efficiency"),
  ("Automated Reporting &amp; KPI Tracking", "BankBazaar · Manager", "Introduced real-time dashboards and scripts so issues surface early and escalations are handled quickly.", "Faster service delivery"),
  ("Verification &amp; Retrieval Automation", "eNoah · USA dental insurance", "Automated repetitive medical-retrieval and verification checks while keeping every step compliant.", "20% client satisfaction"),
  ("Telecom Service Desk Automation", "Lycatel BPO · USA &amp; UK accounts", "Macros, call-routing rules and automated reports that reduced manual effort for a 35-member team.", "15% CSAT · 100% SLA"),
 ],
 tech=[("Automation &amp; Workflow", "Workflow automation, macros and scripting, rule-based call routing"),
       ("Reporting &amp; Analytics", "Automated dashboards, KPI and SLA tracking, MIS reporting"),
       ("Quality &amp; Compliance", "Automated verification checks, QC protocols, regulatory compliance"),
       ("Process Improvement", "Process mapping, gap analysis, SOP documentation, project management")],
 strengths=["Automation-first, process-improvement mindset"] + STRENGTHS_TAIL,
)

CLOUD = dict(
 file="Rajesh_K_M_Resume_Cloud_Enhanced.pdf",
 title="Manager | BPO Operations, Cloud Migration &amp; Solutions",
 tagline="Operations and transformation leader with 18 years of experience across credit card, insurance and telecom BPO, experienced in moving operations and customer data onto cloud platforms while protecting service quality, data security and compliance.",
 stats=[("18+", "Years in BPO &amp; operations"), ("150+", "Team members led"), ("20%", "Growth in acquisition &amp; retention"), ("15%", "Operational efficiency gain"), ("10%", "Lower vendor expenses")],
 timeline=COMMON_TL("35-member team · hosted telephony", "USA dental insurance · hosted systems", "150+ team · cloud migration"),
 summary=[
  "**Operations and transformation leader** across credit card, dental insurance and telecom BPO accounts for USA, UK and Indian clients, including moving contact-centre and back-office operations onto **cloud-based platforms**.",
  "Led migration of operations and customer data to cloud platforms while heading a **team of 150+** in credit card operations, supporting a **20% growth** in customer acquisition and retention.",
  "Owned **cloud solution rollouts** for telephony, CRM and reporting, planning cut-overs and coordinating IT, vendors and users to keep service running without disruption.",
  "Builds **user adoption** through targeted training programs, so teams pick up new platforms quickly and productivity rises.",
  "Keeps **data security and regulatory compliance** in place on hosted systems handling regulated financial and insurance information.",
  "Manages **cloud vendors and costs**: contracts negotiated to **cut expenses by 10%** while upholding service quality and security standards.",
 ],
 competencies=["Cloud Migration Planning", "Cloud Solution Rollout", "Cloud Vendor Management", "Data Security &amp; Compliance", "Cut-over &amp; Change Management", "Remote &amp; Hybrid Enablement", "Operations Management", "Team Leadership", "SLA &amp; KPI Management", "Cost Optimization", "Stakeholder Management", "Project Management", "Training &amp; Adoption"],
 bankbazaar=[
  "Led cross-functional teams through the **migration of operations and customer data to cloud-based platforms**, achieving a **20% growth** in customer acquisition and retention within three years.",
  "Owned **cloud solution rollouts for telephony, CRM and reporting**, boosting operational efficiency by **15%** with significant cost reductions and faster service delivery.",
  "Managed cloud vendor and stakeholder relationships, negotiating contracts that **cut expenses by 10%** while upholding superior service quality and data security standards.",
  "Planned migrations end to end: requirement gathering, cut-over scheduling, data validation and post-go-live support, keeping a **150+ member** credit card operation running without service disruption.",
  "Delivered **targeted training programs** so teams adopted cloud tools quickly, ensuring seamless operations and increased productivity.",
  "Coordinated IT, security, compliance and business stakeholders to keep data protection and regulatory requirements in place through every platform transition.",
  "Tracked KPIs and service levels through cloud-based dashboards, swiftly identifying critical issues, escalating concerns and implementing effective solutions.",
 ],
 enoah=[
  "Led a specialized team in the **USA dental insurance sector**, managing medical retrieval through secure, cloud-hosted repositories and analysis of policies, certificates and renewals, ensuring compliance and accuracy for international clients.",
  "Implemented quality control and **data-security protocols on hosted systems**, maintaining regulatory compliance and boosting the efficiency of medical information retrieval for dental insurance claims.",
  "Worked with vendors and IT partners to migrate hosted platforms and resolve complex cases, **lifting client satisfaction by 20%** in line with industry regulations.",
  "Directed the **Walt Disney E-Publishing Project**, moving publishing and proofreading workflows to shared online platforms for error-free output.",
  "Coordinated project timelines and cross-functional teams to deliver high-quality, brand-consistent content on schedule, upholding Disney’s standards for precision and publishing excellence.",
  "Guided team members through the move to hosted tools with coaching and clear quality standards, sustaining accuracy and productivity.",
 ],
 lycatel=[
  "Led a **team of 35 associates** to consistently exceed key performance indicators (KPIs) in internal customer service operations for USA and UK telecom clients.",
  "Supported the shift of customer service operations from legacy systems to **centralized, hosted telephony and web-based tools**, maintaining service continuity and enhancing customer satisfaction scores by **15%**.",
  "Developed and implemented tailored strategies to meet unique client requirements, achieving **100% compliance** with service level agreements (SLAs) and regulatory standards.",
  "Collaborated cross-functionally with IT and other departments to optimize workflows and platforms, driving a **10% increase in client retention** and overall satisfaction.",
  "Monitored associate performance against KPIs and gave regular feedback, sustaining quality and productivity targets.",
 ],
 cards_title="Cloud &amp; Transformation Initiatives",
 cards=[
  ("Cloud Migration of Credit Card Operations", "BankBazaar · Manager", "Moved operations and customer data to cloud platforms with planned cut-overs, data validation and post-go-live support.", "20% growth · 15% efficiency"),
  ("Cloud Telephony, CRM &amp; Reporting Rollout", "BankBazaar · Manager", "Rolled out cloud solutions with IT and vendors, backed by user training for quick adoption.", "10% lower expenses"),
  ("Secure Cloud-Hosted Retrieval", "eNoah · USA dental insurance", "Ran medical retrieval on secure hosted repositories with data-security and compliance protocols.", "20% client satisfaction"),
  ("Hosted Telephony Transition", "Lycatel BPO · USA &amp; UK accounts", "Supported the move from legacy systems to centralized, hosted telephony and web tools without breaking service continuity.", "15% CSAT · 100% SLA"),
 ],
 tech=[("Cloud Platforms", "Cloud telephony and contact-centre platforms, cloud CRM and reporting"),
       ("Migration &amp; Cut-over", "Migration planning, data validation, cut-over scheduling, post-go-live support"),
       ("Security &amp; Compliance", "Data-security protocols, access control, regulatory compliance on hosted systems"),
       ("Vendor &amp; Cost Management", "Cloud vendor selection, contract and licence negotiation, cost optimization")],
 strengths=["Calm, structured leader through platform transitions"] + STRENGTHS_TAIL,
)

def build(v):
    doc = f"<!doctype html><html><head><meta charset='utf-8'><title>Rajesh K M - Resume</title><style>{CSS}</style></head><body>{page1(v)}{page2(v)}</body></html>"
    (OUT / (v["file"].replace(".pdf", ".html"))).write_text(doc)
    with sync_playwright() as p:
        br = p.chromium.launch(executable_path="/opt/pw-browsers/chromium-1194/chrome-linux/chrome")
        pg = br.new_page(); pg.set_content(doc); pg.wait_for_timeout(300)
        # overflow check: every flex column must fit inside its page
        over = pg.evaluate("""()=>[...document.querySelectorAll('.page')].map((p,i)=>{
          const m=p.querySelector('.main'), s=p.querySelector('.side');
          return {page:i+1, mainOver:m.scrollHeight-m.clientHeight, sideOver:s.scrollHeight-s.clientHeight, mainUsed:[...m.children].reduce((a,c)=>a+c.offsetHeight,0)}})""")
        print(v["file"], over)
        pg.pdf(path=str(OUT / v["file"]), format="A4", print_background=True, prefer_css_page_size=True)
        br.close()

if __name__ == "__main__":
    for v in (AUTOMATION, CLOUD): build(v)
