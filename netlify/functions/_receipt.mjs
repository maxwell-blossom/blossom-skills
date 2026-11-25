// The purchase email: receipt + download + first step. Built as nested tables with inline styles so it renders the same in Gmail, Apple Mail and Outlook.
// receiptEmail({ skill:{id,name,creator,creatorName,prompts}, plan, amount:'9.00 CAD', download, page, mySkills, logo, sessionId, when }) → { subject, html, text }
import { esc } from './_mail.mjs';
const PURPLE = '#7361F7', INK = '#171717', MUTED = '#72777F', BG = '#F1F5F7', BORDER = '#E3E3E3';
export function receiptEmail({ skill: s, plan, amount, download, page, mySkills, logo, sessionId, when }) {
  const planTxt = plan === 'once' ? 'One-time purchase' : plan === 'monthly' ? 'Monthly subscription' : 'Yearly subscription';
  const prompt = (s.prompts || [])[0] || 'Run ' + s.name;
  const by = s.creatorName ? `${s.creatorName} (@${s.creator})` : '@' + s.creator;
  const date = (when || new Date()).toLocaleDateString('en-CA', { month: 'long', day: 'numeric', year: 'numeric' });
  const keep = plan === 'once' ? 'Your download link works for 12 months and every update in that time is included.' : `Every update is included while you’re subscribed. Change or cancel any time from <a href="${mySkills}" style="color:${PURPLE}">My skills</a>.`;
  const row = (k, v) => `<tr><td style="padding:6px 0;color:${MUTED};font-size:14px">${k}</td><td align="right" style="padding:6px 0;color:${INK};font-size:14px;font-weight:700">${v}</td></tr>`;
  const html = `<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>${esc(s.name)} · Blossom Skills</title></head>
<body style="margin:0;padding:0;background:${BG}">
<table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background:${BG}"><tr><td align="center" style="padding:28px 16px">
<table role="presentation" width="560" cellpadding="0" cellspacing="0" style="max-width:560px;width:100%;font-family:Nunito,'Helvetica Neue',Helvetica,Arial,sans-serif">
  <tr><td style="padding:0 4px 18px"><img src="${logo}" width="132" height="34" alt="Blossom" style="display:block;border:0"></td></tr>
  <tr><td style="background:#ffffff;border:1px solid ${BORDER};border-radius:16px;padding:28px 28px 24px">
    <div style="font-size:12px;font-weight:800;letter-spacing:.4px;text-transform:uppercase;color:${PURPLE}">Blossom Skills · receipt</div>
    <h1 style="font-size:24px;line-height:1.25;margin:10px 0 6px;color:${INK}">You’re in. ${esc(s.name)} is yours.</h1>
    <p style="margin:0 0 20px;color:${MUTED};font-size:15px">By ${esc(by)}</p>
    <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="border-top:1px solid ${BORDER};border-bottom:1px solid ${BORDER};margin:0 0 22px">
      ${row('Plan', esc(planTxt))}${row('Paid', esc(amount))}${row('Date', esc(date))}
    </table>
    <table role="presentation" cellpadding="0" cellspacing="0"><tr><td style="background:${PURPLE};border-radius:999px"><a href="${download}" style="display:inline-block;padding:14px 26px;color:#ffffff;font-weight:700;font-size:16px;text-decoration:none">Download SKILL.md</a></td></tr></table>
    <p style="margin:12px 0 0;color:${MUTED};font-size:13px">Also in <a href="${mySkills}" style="color:${PURPLE}">My skills</a> on any device you’re signed in to.</p>
  </td></tr>
  <tr><td style="height:14px"></td></tr>
  <tr><td style="background:#ffffff;border:1px solid ${BORDER};border-radius:16px;padding:24px 28px">
    <div style="font-size:16px;font-weight:800;color:${INK};margin:0 0 12px">Next: add it to Claude</div>
    <table role="presentation" cellpadding="0" cellspacing="0" style="font-size:14.5px;line-height:1.5;color:${INK}">
      <tr><td valign="top" style="padding:0 10px 10px 0;color:${PURPLE};font-weight:800">1</td><td style="padding:0 0 10px">Put <code style="font-family:Menlo,Consolas,monospace;font-size:13px;background:${BG};padding:1px 5px;border-radius:4px">SKILL.md</code> in a folder named <code style="font-family:Menlo,Consolas,monospace;font-size:13px;background:${BG};padding:1px 5px;border-radius:4px">${esc(s.id)}</code> and zip it.</td></tr>
      <tr><td valign="top" style="padding:0 10px 10px 0;color:${PURPLE};font-weight:800">2</td><td style="padding:0 0 10px">In Claude: <b>Settings → Capabilities → Skills → Upload skill</b>, choose the zip. <span style="color:${MUTED}">(In the desktop app or Claude Code you can also drop the file into a chat and say “Save this as a skill.”)</span></td></tr>
      <tr><td valign="top" style="padding:0 10px 0 0;color:${PURPLE};font-weight:800">3</td><td>Ask: <i>“${esc(prompt)}”</i></td></tr>
    </table>
    <p style="margin:14px 0 0;color:${MUTED};font-size:13.5px">Using Claude Code, Cursor, ChatGPT or Grok instead? The steps for each are on <a href="${page}" style="color:${PURPLE}">the skill page</a>.</p>
  </td></tr>
  <tr><td style="padding:18px 6px 0;color:${MUTED};font-size:12.5px;line-height:1.5">
    ${keep}<br>
    Receipt ${esc(sessionId)} · Questions or refunds: <a href="mailto:skills@blossomsocial.com" style="color:${PURPLE}">skills@blossomsocial.com</a><br>
    Blossom Social Inc. · 49 Spadina Ave, Toronto ON M5V 0K3
  </td></tr>
</table></td></tr></table></body></html>`;
  const text = `You're in. ${s.name} is yours.
By ${by}

Plan: ${planTxt}
Paid: ${amount}
Date: ${date}

Download SKILL.md: ${download}
(Also in My skills on any device: ${mySkills})

Next: add it to Claude
1. Put SKILL.md in a folder named ${s.id} and zip it.
2. In Claude: Settings → Capabilities → Skills → Upload skill, choose the zip. (In the desktop app or Claude Code you can also drop the file into a chat and say "Save this as a skill.")
3. Ask: "${prompt}"
Claude Code, Cursor, ChatGPT or Grok: ${page}

${keep.replace(/<[^>]+>/g, '')}
Receipt ${sessionId} · Questions or refunds: skills@blossomsocial.com
Blossom Social Inc. · 49 Spadina Ave, Toronto ON M5V 0K3`;
  return { subject: `Your receipt · ${s.name} on Blossom Skills`, html, text };
}
