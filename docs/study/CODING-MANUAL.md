# Coding manual: indicator presence coding

**Status: DRAFT manual for a draft protocol that has not been run. It may be revised once after the pilot and is then frozen. See `PROTOCOL.md`.**

Every example in this manual is fictional. The people, places, and events were invented for illustration and describe no real case.

## 1. Your task

You will read a short written case narrative and decide, for each indicator in one matrix, whether the narrative shows that behavior. You record one code per indicator. You work alone. You are not being asked whether the subject was dangerous, what should have been done, or how serious anything was.

You are coding the text in front of you, not the case as you may know it from elsewhere.

## 2. How to read an indicator

Each indicator is one sentence describing an observable behavior. It sits inside a tactic, which has a name and notes.

1. **Read the whole sentence.** Most indicators have an actor, an action, an object, and often a qualifier ("sustained", "repeated", "with no apparent legitimate purpose", "outside the scope of their job function"). Every part must be met, including the qualifier.
2. **Lists joined by "or" are alternatives.** One item is enough. Lists joined by "and" require all items.
3. **Text after a colon or "including" gives examples**, not a closed list. A behavior of the same kind that is not listed still counts.
4. **Use the tactic notes for scope.** If two indicators look alike, the tactic notes usually say what separates them (for example remote research versus physical presence, or rehearsal versus the live approach).
5. **"Threat actor" is the vocabulary's label for whoever carries out the behavior.** In this study read it as "the subject of the narrative". The label is not a finding about the person.
6. **Do not use any knowledge of scores or priorities.** You will not be shown any, and none applies to this task.

## 3. The three codes

| Code | Use it when |
|---|---|
| `present` | The narrative states the behavior, or states facts that together amount to it, and you can quote the passage |
| `absent` | The narrative gives a reasonably full account of the period or setting where the behavior would appear, and does not show it |
| `cannot_determine` | The narrative is silent or too thin on the matter for you to say either way |

Choosing between `absent` and `cannot_determine`:

- Ask: "If the subject had done this, would this narrative be expected to say so?" If yes and it does not, code `absent`. If the narrative simply does not cover that period, place, or kind of information, code `cannot_determine`.
- A narrative that covers the weeks before an event in detail and never mentions weapons supports `absent` for weapons acquisition. A narrative that begins on the day of the event supports only `cannot_determine` for anything earlier.
- Indicators about what happened after an event are `cannot_determine` if the narrative has no post-event section.
- `cannot_determine` is not a safe middle option. Use it when the text does not let you decide, and say why in the note field when the reason is not obvious.

When the evidence is mixed, pick the code you would defend and set confidence to low. Do not use `cannot_determine` to express low confidence in a `present` or `absent` judgment.

## 4. The evidence passage

Every `present` needs a passage.

- Quote the narrative **verbatim**. Do not paraphrase, summarise, or correct.
- Quote the **shortest** passage that shows the behavior, normally one to three sentences. If two separate passages are both needed, quote both separated by " [...] ".
- The passage must come from the **narrative**, not from the underlying source documents, your memory, or another case.
- Add a paragraph reference in the locator field if the narrative has numbered paragraphs.
- If you cannot find a passage to quote, the code is not `present`.

`absent` and `cannot_determine` need no passage.

## 5. Inference

You may draw an inference that any careful reader would draw from the stated facts. You may not fill gaps.

Allowed:

- **Direct statement.** The narrative says the subject did the thing.
- **Necessary implication.** The stated facts cannot be true unless the behavior occurred. "The subject arrived wearing a courier uniform; the subject had never worked for a courier" implies adopting a uniform inconsistent with actual employment.
- **Attributed findings.** If the narrative reports that a court or commission found a fact, treat the fact as stated.

Not allowed:

- **Outcome reasoning.** "There must have been planning because of what happened later." Code only what the narrative shows.
- **Typical-case reasoning.** "People who do X usually also do Y."
- **Motive or state of mind** that the narrative does not state. Where an indicator turns on purpose ("to detect surveillance", "to avoid detection"), the narrative must state the purpose, or state facts that leave no ordinary explanation. If an ordinary explanation remains open, code `absent` or `cannot_determine` under section 3.
- **Outside knowledge**, including anything you remember about the real case if you recognise it.
- **Upgrading an attempt or a statement into an act.** Saying one will buy a weapon is a communication, not an acquisition. Where an indicator says "obtains or attempts to obtain", an attempt counts; where it says "acquires", it does not.

Qualifiers such as "sustained", "repeated", or "multiple occasions" need at least two distinct instances in the narrative unless the narrative itself uses an equivalent word.

## 6. Overlapping indicators

Indicators are written to be distinct, but one passage can satisfy more than one.

- **Code each indicator on its own terms.** If one passage meets two indicators, code both `present` and quote the same passage for each. Do not ration.
- **Do not let one code imply another.** A `present` on a specific indicator does not make a broader neighbouring indicator `present` unless the passage also meets the broader wording, and the reverse.
- **Summary-style indicators.** Some tactics include an indicator that describes a general pattern (for example "engages in preparation behavior") alongside tactics that hold the specific behaviors. Code the general indicator `present` only when the passage meets its own sentence, not merely because a specific indicator elsewhere is `present`.
- **Same behavior, different phase.** Several tactics describe similar acts at different stages (reconnaissance visit, rehearsal, final approach). Use the tactic notes and the narrative's timeline. If the narrative does not let you tell the stages apart, code the earliest stage the text supports and use `cannot_determine` for the later ones.
- **Cross-matrix lookalikes.** You are coding one matrix per case. Ignore the other matrix.
- **When torn between two indicators**, code what each sentence requires, then use the note field to record the neighbour you considered. These notes are used to improve wording.

## 7. Confidence

Record your confidence in each code.

| Level | Meaning |
|---|---|
| high | The text plainly meets, or plainly does not meet, the indicator |
| medium | A careful reader could go the other way, but you would defend your code |
| low | You had to choose; the wording or the text left real doubt |

Confidence is about your reading, not about how alarming the behavior is.

## 8. Worked micro-examples (fictional)

These use invented text and two real indicator sentences so you can see the rule applied. They are not cases.

**Example A. Direct statement.**
Narrative text: "Over three weeks in March the subject searched online for the home address of the regional manager, the manager's usual gym, and the school the manager's children attended, and saved the results in a folder."
Indicator IND-0101-02 (sustained online research into a specific individual's personal details, schedule, residence, workplace, family members, associated venues, or daily routines): `present`, high. Passage: the sentence quoted. "Over three weeks" meets "sustained".

**Example B. One instance does not meet "sustained".**
Narrative text: "On 4 March the subject looked up the regional manager's office address on the company website."
IND-0101-02: `absent`, medium, if the narrative covers the subject's online activity in the period; `cannot_determine` if this is the only mention of online activity and the narrative does not say it had access to more. Either way it is not `present`: one lookup of a workplace address is not sustained research.

**Example C. Statement is not acquisition.**
Narrative text: "The subject told a neighbour that he was 'going to get a rifle soon'."
An indicator about acquiring weapons: not `present`. An indicator about communicating intent to a third party may be `present` if its own wording is met (a rifle remark with no target named would not meet an indicator that requires intent "regarding a specific individual, role, or group").

**Example D. Purpose not stated.**
Narrative text: "The subject drove to the clinic by a different route on each of four visits."
Indicator IND-0108-01 (varies vehicle, route, or arrival time across repeated visits "in a pattern consistent with deliberate surveillance detection"): the variation is stated, nothing ties it to surveillance detection, and ordinary explanations remain. Code `absent` if the narrative otherwise covers the subject's reasons, else `cannot_determine`, with a note. If the narrative added "and told a friend he changed routes so nobody could follow him", code `present`.

**Example E. Overlap.**
Narrative text: "The subject wore a hi-vis vest and carried a clipboard, told the receptionist he was there to inspect the fire extinguishers, and was let through to the second floor. No inspection had been booked."
Several indicators can be `present` on this one passage: adopting attire inconsistent with actual role; a stated reason that does not match verifiable activity; using a pretext to pass a staffed access point. Code each against its own sentence and quote the passage for each.

**Example F. Silence.**
Narrative text covers only the morning of the event.
Every indicator about research, acquisition, or rehearsal in earlier weeks: `cannot_determine`. Note: "narrative begins on day of event".

**Example G. Non-event.**
Narrative text: "Investigators reviewed the subject's devices, purchases, and movements for the preceding six months and found no searches about the complainant, no weapon purchases, and no visits to her workplace."
Indicators about online research into the person, weapon acquisition, and appearing at associated locations: `absent`, high. The narrative says the matter was looked at and nothing was found.

## 9. Procedure for each case

1. Record whether you recognise the case (yes, no, unsure). Then set that aside.
2. Read the whole narrative once before coding anything.
3. Work through the matrix tactic by tactic. Read the tactic notes, then code each indicator.
4. For each `present`, paste the passage. For any `cannot_determine` whose reason is not obvious, add a note.
5. If the narrative has a separate post-event section, code the pre-event tactics first, then read that section and code the remaining tactics. Do not go back and change earlier codes because of what the later section says.
6. Check that every indicator has a code and every `present` has a passage. Submit. Files are final on submission.

## 10. What not to do

- Do not discuss cases or codes with other raters until the coordinator confirms all coding is complete.
- Do not look up the case, the sources, or the people.
- Do not record any opinion about risk, seriousness, or what should have been done.
- Do not use tools that suggest codes for you.
- If you realise you have a personal or professional connection to a case, stop and tell the coordinator.

## 11. Questions

Send questions about the manual to the coordinator in writing. If the answer clarifies a rule it is sent to every rater and logged. The coordinator will not answer questions about how to code a particular passage.
