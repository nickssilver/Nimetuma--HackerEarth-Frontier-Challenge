# Improvement changelog

Same 10 cases for every row. Primary metric: verdict match against gold. Secondary: false paid (the seller would have lost goods).

| Stage | What you tried and why | Evidence | Decision / learning |
| --- | --- | --- | --- |
| Baseline | One pass over the chat. If they said *nimetuma* or sent a screenshot, call it paid. This is how a rushed seller actually decides. | 3/10 correct. 7/10 false paid. | Established the starting point. Trust is not a till. |
| Iteration 1 | Parse screenshot SMS as if it were a till row. Better context, still no statement. | 7/10. False paid fell to 3/10 (cases 02, 07, 10). Case 05 survived because 5,000 did not match a 500 order. | Kept the parser. Removed screenshot-as-evidence. A well-formed fake still empties the shop. |
| Iteration 2 | Query the till. Freshness window 45 minutes. Recycled SMS from 28 Aug fails today's chat. | 9/10. False paid 0. Case 04 broke: spouse paid, name order flipped, chat only said *mke wangu*. | Kept till-first verification. Identity cannot be chat-only. |
| Iteration 3 | Added memory of known family numbers and Kenyan name-order matching. | Case 04 flipped to paid. Still 9/10 because iteration 4 was not in yet. | Kept memory for identity. Never use it to fill an empty till. |
| Iteration 4 (removed) | If the chat is fluent Sheng or Kiswahili and the number is a regular, trust *nimetuma* when the till is quiet. Neighbors do not lie. | 9/10. False paid returned: case 10, Janet, *niko hurry*, empty till, predicted paid. | Removed. Fluency made the agent easier to con. Language comfort is a risk. |
| Final | Combine till-first verify, memory for identity only, reply in the customer's register, human checkpoint before release. | **10/10. False paid 0.** See `results/eval.json`. | Main contribution: refuse screenshots, then write the human no. |

## Per-case final verdicts

All ten match gold. Trajectories are in `trajectories/final/`.

| Case | Gold | Final | What it is |
| --- | --- | --- | --- |
| 01 | paid | paid | Real send, fresh SMS |
| 02 | not_paid | not_paid | Edited screenshot, empty till |
| 03 | not_paid | not_paid | Recycled SMS from 28 Aug |
| 04 | paid | paid | Spouse, name order flipped |
| 05 | not_paid | not_paid | Change scam |
| 06 | paid | paid | Honest eight-minute delay |
| 07 | not_paid | not_paid | Lookalike till |
| 08 | unclear | unclear | Partial 1,000 of 2,400 |
| 09 | unclear | unclear | Inbound then reversal |
| 10 | not_paid | not_paid | Regular, rushed, empty till |

## Main failure mode

A fluent regular on an empty till. The agent that "understood" the customer was the one that paid them.

## Hot take

Sheng and Kiswahili did not make the agent more honest. They made it more trusting. The scammer already sounds like a neighbor. Verification has to treat language comfort as a risk until the till row exists. Amina still confirms. The agent never releases the goods.
