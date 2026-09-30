"""Build the two Rajesh K M resume variants from the original PDF.

The original layout is kept intact: only the profile photo, the profile summary
and the job bullets are replaced. Employers, titles, dates and every metric that
appeared in the original are preserved.

Usage: python3 build_resumes.py ORIGINAL.pdf OUT_DIR
"""
import sys
import pymupdf

SRC, OUT = sys.argv[1], sys.argv[2]
PHOTO = __file__.rsplit("/", 1)[0] + "/photo_trimmed_mustache.jpg"
FONT = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"  # Arial-metric
INK = (0x1C / 255, 0x20 / 255, 0x29 / 255)
LEAD, SIZE = 15.6, 12.0
font = pymupdf.Font(fontfile=FONT)


def wrap(text, first_w, next_w):
    """Greedy wrap; first line is narrower because of the '- ' bullet."""
    words, lines, cur = text.split(), [], ""
    for w in words:
        limit = first_w if not lines else next_w
        trial = (cur + " " + w).strip()
        if font.text_length(trial, SIZE) <= limit:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    return lines


def bullets_to_lines(bullets, gap):
    """-> list of (is_first_line_of_bullet, text) with optional blank spacer lines."""
    out = []
    for i, b in enumerate(bullets):
        if gap and i:
            out.append((None, ""))
        for j, ln in enumerate(wrap(b, 571 - 223.3, 571 - 214.9)):
            out.append((j == 0, ln))
    return out


def draw(page, lines, y0):
    for first, ln in lines:
        if first is not None:
            base = y0 + 0.905 * SIZE
            if first:
                page.insert_text((214.9, base), "-", fontsize=SIZE, fontname="lsans", fontfile=FONT, color=INK)
                page.insert_text((223.3, base), ln, fontsize=SIZE, fontname="lsans", fontfile=FONT, color=INK)
            else:
                page.insert_text((214.9, base), ln, fontsize=SIZE, fontname="lsans", fontfile=FONT, color=INK)
        y0 += LEAD
    return y0


def build(variant, out_name, title):
    doc = pymupdf.open(SRC)
    p1, p2 = doc[0], doc[1]

    # 1) clear the text we are replacing (graphics/backgrounds are untouched)
    for page, rects in ((p1, [(148, 66, 575, 246), (212, 497, 580, 690), (212, 705, 580, 830)]),
                        (p2, [(212, 10, 580, 205), (212, 218, 580, 420)])):
        for r in rects:
            page.add_redact_annot(pymupdf.Rect(*r))
        page.apply_redactions(images=pymupdf.PDF_REDACT_IMAGE_NONE,
                              graphics=pymupdf.PDF_REDACT_LINE_ART_NONE)

    # 2) profile photo with the mustache trimmed to the lip
    p1.replace_image(18, filename=PHOTO)

    # 3) profile summary
    lines = wrap(variant["summary"], 535 - 150.1, 535 - 150.1)
    assert len(lines) <= 11, ("summary too long", len(lines))
    y = 69.6
    for ln in lines:
        p1.insert_text((150.1, y + 0.905 * SIZE), ln, fontsize=SIZE, fontname="lsans", fontfile=FONT, color=INK)
        y += LEAD
    print(out_name, "summary lines:", len(lines))

    # 4) BankBazaar (page 1)
    bb = bullets_to_lines(variant["bankbazaar"], gap=True)
    assert len(bb) <= 11, ("BankBazaar too long", len(bb))
    draw(p1, bb, 501.4)

    # 5) eNoah: flows from the bottom of page 1 onto the top of page 2, as in the original
    en = bullets_to_lines(variant["enoah"], gap=False)
    on_p1, on_p2 = en[:7], en[7:]
    assert len(on_p2) <= 11, ("eNoah too long", len(on_p2))
    draw(p1, on_p1, 709.4)
    draw(p2, on_p2, 15.8)

    # 6) Lycatel (page 2)
    ly = bullets_to_lines(variant["lycatel"], gap=False)
    assert len(ly) <= 14, ("Lycatel too long", len(ly))
    draw(p2, ly, 223.4)
    print(out_name, "lines  BB/eNoah/Lycatel:", len(bb), len(en), len(ly))

    doc.set_metadata({"title": title, "author": "Rajesh K M", "subject": "Resume"})
    doc.save(f"{OUT}/{out_name}", garbage=3, deflate=True)


AUTOMATION = dict(
    summary=(
        "BPO operations leader with 18 years of experience driving process "
        "automation across credit card, insurance and telecom operations. Led "
        "teams of 150+ while replacing manual, repetitive work with automated "
        "workflows, scripts and reporting dashboards that improved accuracy, "
        "turnaround time and productivity. Skilled at spotting automation "
        "opportunities, partnering with IT and vendors to implement them, and "
        "training teams to adopt new tools. Proven record in process "
        "improvement, SLA compliance and operational excellence in fast-paced "
        "financial services environments."
    ),
    bankbazaar=[
        "Led cross-functional teams to automate application submission and "
        "lead-processing workflows, achieving a 20% growth in customer "
        "acquisition and retention within three years.",
        "Replaced manual, repetitive processes with automation, scripts and "
        "real-time dashboards, boosting operational efficiency by 15% with "
        "significant cost reductions and faster service delivery.",
        "Managed vendor and stakeholder relationships for automation tools, "
        "negotiating contracts that cut expenses by 10% while upholding "
        "superior service quality standards.",
    ],
    enoah=[
        "Led a specialized team in the USA dental insurance sector, managing "
        "medical retrieval processes through detailed analysis of policies, "
        "certificates, and renewals, automating repetitive steps to ensure "
        "compliance and accuracy for international clients.",
        "Implemented quality control protocols with automated verification "
        "checks, maintaining regulatory compliance and boosting the efficiency "
        "of medical information retrieval essential for dental insurance claims.",
        "Worked with vendors to automate case hand-offs and resolve complex "
        "cases, streamlining service delivery and increasing client "
        "satisfaction by 20%, in line with industry regulations.",
        "Directed the Walt Disney E-Publishing Project, automating content "
        "publishing steps and proofreading checks to ensure error-free output.",
        "Coordinated project timelines and cross-functional teams to deliver "
        "high-quality, brand-consistent content on schedule, upholding "
        "Disney’s standards for precision and publishing excellence.",
    ],
    lycatel=[
        "Led a team of 35 associates to consistently exceed key performance "
        "indicators (KPIs) in internal customer service operations for USA and "
        "UK telecom clients.",
        "Introduced macros, call-routing rules and automated reports to cut "
        "manual effort, enhancing customer satisfaction scores by 15% and "
        "surpassing client expectations for international accounts.",
        "Developed and implemented tailored strategies and automated tracking to "
        "meet unique client requirements, achieving 100% compliance with service "
        "level agreements (SLAs) and regulatory standards.",
        "Collaborated cross-functionally with various departments to optimize "
        "and automate workflows, driving a 10% increase in client retention and "
        "overall satisfaction.",
    ],
)

CLOUD = dict(
    summary=(
        "BPO operations and transformation leader with 18 years of experience, "
        "including moving contact-centre and back-office operations onto "
        "cloud-based platforms. Led teams of 150+ in credit card operations "
        "while managing cloud migration planning, vendor selection, data "
        "security and compliance, and user training with minimal disruption to "
        "service. Skilled in cloud solutions for telephony, CRM and remote "
        "working, cost optimization and stakeholder management across "
        "financial services, insurance and telecom clients."
    ),
    bankbazaar=[
        "Led cross-functional teams through the migration of operations and "
        "customer data to cloud-based platforms, achieving a 20% growth in "
        "customer acquisition and retention within three years.",
        "Owned cloud solution rollouts for telephony, CRM and reporting, "
        "boosting operational efficiency by 15% with significant cost "
        "reductions and faster service delivery.",
        "Managed cloud vendor and stakeholder relationships, negotiating "
        "contracts that cut expenses by 10% while upholding superior service "
        "quality and data security standards.",
    ],
    enoah=[
        "Led a specialized team in the USA dental insurance sector, managing "
        "medical retrieval through secure, cloud-hosted repositories and "
        "analysis of policies, certificates, and renewals, ensuring compliance "
        "and accuracy for international clients.",
        "Implemented quality control and data-security protocols on hosted "
        "systems, maintaining regulatory compliance and boosting the efficiency "
        "of medical information retrieval for dental insurance claims.",
        "Worked with vendors and IT partners to migrate hosted platforms and "
        "resolve complex cases, lifting client satisfaction by 20% in line with "
        "industry regulations.",
        "Directed the Walt Disney E-Publishing Project, moving publishing and "
        "proofreading workflows to shared online platforms for error-free output.",
        "Coordinated project timelines and cross-functional teams to deliver "
        "high-quality, brand-consistent content on schedule, upholding "
        "Disney’s standards for precision and publishing excellence.",
    ],
    lycatel=[
        "Led a team of 35 associates to consistently exceed key performance "
        "indicators (KPIs) in internal customer service operations for USA and "
        "UK telecom clients.",
        "Supported the shift of customer service operations from legacy systems "
        "to centralized, hosted telephony and web-based tools, maintaining "
        "service continuity and enhancing customer satisfaction scores by 15%.",
        "Developed and implemented tailored strategies to meet unique client "
        "requirements, achieving 100% compliance with service level agreements "
        "(SLAs) and regulatory standards.",
        "Collaborated cross-functionally with IT and other departments to "
        "optimize workflows and platforms, driving a 10% increase in client "
        "retention and overall satisfaction.",
    ],
)

if __name__ == "__main__":
    build(AUTOMATION, "Rajesh_K_M_Resume_Automation.pdf", "Rajesh K M - Resume (BPO Process Automation)")
    build(CLOUD, "Rajesh_K_M_Resume_Cloud.pdf", "Rajesh K M - Resume (BPO Cloud Migration & Solutions)")
