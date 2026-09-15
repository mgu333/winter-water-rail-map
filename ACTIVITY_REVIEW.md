# 100 activity candidates — review edition

This is a discovery list, not a scientifically scored top 100 or evidence that every activity is available today.

- 100 distinct pictorial symbols, with stable ID badges.
- 26 mentioned interests, 39 related ideas, and 35 intuition-led ideas.
- 87 approximate site/campus reference pins; 13 ideas explicitly await a verified local venue or legal access point.
- Three independently modeled travel modes for every mapped candidate. Walking and cycling outside the 15/30-minute daily limits are grayed out, not recommended as practical trips.
- Drive filters: 2 hours, or a 2.5-hour stretch. Routing does not include traffic, parking, registration or activity duration.
- Review controls: Keep, Maybe, Possible duplicate, Skip. Choices remain in local browser storage; export creates a review file, not an upload.
- Shared locations cluster on the map and separate when zoomed/clicked. The full review grid exposes all 100 regardless of overlap or location status.

## Personalization and privacy

The list draws on the user's stated ocean, outdoor, food and learning priorities, selected accessible Gemini conversations, and Claude Code's saved interest notes. AI-generated suggestions in old chats are not treated as proof of the user's preferences. Intuition-led choices are explicitly labeled. Private conversation excerpts, medical details and actual residential information are not included.

The origin is the same illustrative Pacific Grove / New Monterey point used previously, not a chosen home. Location coordinates are approximate reference points, not surveyed or fully verified entrances. Campus entries do not guarantee an available class; see each entry's source and access notes.

## Important gaps

Sepak takraw, deep-water soloing, several harvesting activities, and some specialist classes remain in the review inventory without fabricated map pins or routes. An unmapped essential activity should count against the proposed home base, not be silently assumed available. Food harvesting must satisfy current protected-area boundaries, species, season, gear and health rules. No claim is made that wild harvesting can replace all groceries.

The original winter railway alignment and six directional driving routes remain unchanged. The inherited 2070 county overlay remains a labeled illustrative scenario, not a validated local projection.

## Rebuild

`activity-picks.json` contains the public candidate metadata. `expand_candidates.mjs` rebuilds the 100-entry inventory; `build_routes.py` fills mode-specific routes from its local cache or Valhalla. The route builder preserves existing rail geometry. `activities-ui.js` adds the icon and manual-review interface.

Icons use Twemoji SVGs with native emoji fallback (Twemoji graphics CC-BY 4.0; https://github.com/jdecked/twemoji). Map/routing credits appear in the map.
