# Outreach kit: get the Rutgers facts by Oct 31 (Gate A)

Primary data is the one thing other teams' LLMs cannot produce. Send these on **Oct 21–22**, copy the faculty sponsor, and log every reply in `field_data/outreach_log.csv` (date, office, ask, answer, follow-up).

**Never** put lifeline locations in public documents. Ask for **counts by type**. Locations stay with Facilities and are not needed for the pitch.

---

## 1. Faculty sponsor (send first; everything else goes out with their name on it)
**To:** a WINLAB / ECE faculty member (ideally someone who already knows the Verizon challenge)
**Subject:** Verizon Smart Campus Challenge: co-sign a facts request to OIT and Facilities?

> Professor ___,
>
> Our team is entering the Verizon Smart Campus Innovation Challenge (video due Nov 8). Our entry is about Verizon's copper retirement. Verizon has filed a public notice (No. 2026-03-A-NJ, Sept 8, 2026) retiring copper "at all remaining locations" in 62 New Jersey wire centers, including Piscataway, on or after Dec 10, 2026. Elevator emergency phones, fire-alarm communicators and similar life-safety devices have traditionally used copper phone lines.
>
> We would like to ask OIT Telecom and Facilities two questions: how many such lines Rutgers still has on Verizon copper in Piscataway, and who answers elevator emergency calls. We would ask only for counts, never locations. Would you be willing to be copied as our faculty sponsor? We can send you a one-page summary.
>
> Thank you, ___

## 2. OIT Telecom (voice services)
**Subject:** Student research question: analog/copper lines in Piscataway before Verizon's Dec 10 copper retirement

> Hello,
>
> We are a student team (faculty sponsor: ___) studying how campuses get ready for copper retirement. Verizon's public notice 2026-03-A-NJ lists the Piscataway wire center (4 Skiles Ave) for copper retirement on or after Dec 10, 2026. New Brunswick is not on the list.
>
> We would be grateful for **counts only**, no locations or numbers:
> 1. Roughly how many Verizon analog/copper lines does Rutgers still have at Busch, Livingston and other Piscataway addresses?
> 2. Roughly how are they used? Elevator phones, refuge/area-of-rescue call boxes, fire-alarm communicators, intrusion alarms, blue-light phones, fax or modem, or other.
> 3. Has Verizon contacted Rutgers about migrating them, and is a plan in place (cellular gateways, the campus network, another carrier)?
> 4. Are campus elevator phones on Verizon lines, on the Rutgers phone system, or on a monitoring provider's lines?
>
> A 15-minute call would also be wonderful. Thank you, ___

## 3. Facilities: elevator shop, and fire-alarm/life-safety shop
**Subject:** Elevator emergency phones: who answers, and how are they tested?

> Hello,
>
> We are a student team (faculty sponsor: ___) working on elevator emergency-phone reliability for the Verizon Smart Campus Challenge. Three questions:
> 1. When someone presses HELP in a campus elevator, where does the call go: RUPD dispatch, the elevator contractor's call center, or a monitoring company?
> 2. How are the phones tested today, and how often? For example: annual inspection, monthly checks, or automatic line monitoring.
> 3. Would Facilities allow a **pre-announced, supervised** test? A Facilities staff member would press HELP in 10–20 elevators during a window agreed with whoever answers, so we can time the answer and check that the building and car are known. We would share all results with Facilities privately first.
>
> We will not touch any equipment. Thank you, ___

## 4. RUPD / Rutgers emergency communications
**Subject:** Student research: elevator emergency calls and location information

> Hello,
>
> We are a student team (faculty sponsor: ___) studying elevator emergency calls on campus. Could someone tell us:
> 1. Whether elevator HELP calls reach RUPD dispatch, and what the dispatcher sees (a building or car label, or only a phone number)?
> 2. Whether you would be willing to take part in a short, pre-announced test window organized with Facilities?
>
> We will never place a test call to 911 or to RUPD without your written agreement and an agreed window. Thank you, ___

## 5. Office of Disability Services
**Subject:** Deaf/hard-of-hearing input on a text mode for elevator emergency phones

> Hello,
>
> New Jersey's 2026 building-code update brings in the requirement that elevator emergency communication be both visual and audible, so Deaf, hard-of-hearing and speech-impaired riders can use it. Our student team is prototyping a text mode for the HELP button.
>
> Could you connect us with a Deaf or hard-of-hearing student, or a staff member, willing to give 20 minutes of feedback on the wording and the flow? Participation is voluntary, and we will request an IRB determination before any formal study.
>
> Thank you, ___

## 6. OPRA request (NJ Open Public Records Act; Rutgers records custodian)
File through Rutgers' OPRA portal. Keep the request narrow so it is not denied as overbroad. Expect the security-records exemption to cover locations, which is why we ask only for counts and invoices.

> Under OPRA (N.J.S.A. 47:1A-1 et seq.), I request:
> 1. The most recent monthly invoice(s), summary pages only, from Verizon New Jersey Inc. to Rutgers, The State University of New Jersey, for local exchange telephone service billed to service addresses in Piscataway Township. If line-level detail is included, please redact service addresses and telephone numbers and provide only the line or service type codes and counts.
> 2. Any written notice received from Verizon between June 1, 2026 and today about copper retirement or service discontinuance affecting Rutgers lines (Verizon notice 2026-03-A-NJ or related), with security-sensitive details redacted.
> 3. Any contract, purchase order or invoice from Jan 1, 2025 to today for elevator emergency phone monitoring or for POTS-line replacement (cellular communicators or gateways).
>
> Electronic copies preferred.

## 7. HELP-button audit protocol (only with written Facilities permission)
- **Who presses:** a Facilities staff member, or a student with Facilities staff present. Never press HELP unannounced.
- **Window:** agreed in writing with the answering point, who also confirms the window again by phone on the day.
- **Per car, record:** building and car (as labeled), time pressed, rings until answered, seconds to answer, who answered, whether they knew the building or car without asking, the audio quality both ways (1–5), whether a visual indicator lit, and whether text or visual communication is available.
- **Say:** "This is a pre-arranged test with Facilities, there is no emergency." Then hang up politely.
- **Data:** keep it only in `field_data/help_audit.csv`, and share it only in aggregate. No faces, and no recording of the answerer's voice.

## 8. Machine-room LTE-M survey (only with an escort)
- **Where:** in or next to the elevator controller or machine room. If there is no access, measure at the nearest public point and label it a proxy.
- **Measure:** Verizon RSRP, RSRQ and SINR, the band, and LTE vs 5G on a Verizon phone, plus one other carrier as a control ("Carrier B"). If the dev kit has arrived, also record LTE-M attach success and time-to-attach.
- **Columns:** reuse `deliverables/FIELD_KIT_OCT31.md` and add `location_type` (machine_room, controller_closet, lobby_proxy, car) and `attach_ok`.
- **Analyze:** `python3 scripts/analyze_walktest.py field_data/<file>.csv`

## 9. Car-station walk audit (public elevators, visual only, no permission needed)
- **Per car, record:** building, car, phone type (push-button hands-free or handset), whether a display or text screen is present, whether the ADA signage or tactile marking is present, and the visible maker or model.
- **Purpose:** gives the baseline for "visual + audible" (IBC 3001.2) and the phone population for PROVE.
- **Do not:** photograph people, or open any panel.
