# ByteWise daily video playbook

For the scheduled runs. Channel: ByteWise (@heybytewise), YouTube + Instagram, India audience, faceless, English only, voice only (no music, no sound effects).

Publishing is ONE-TAP: prepare the post, then publish only after the user replies "post it" (or similar clear approval) in this run's chat. Never publish without that reply. Never spend vidIQ or Higgsfield credits (uploads, drafts and YouTube/Instagram publishing are free; X posts cost credits, so never post to X). Never print or save the Pixabay key anywhere; it comes in the task prompt and only goes into the PIXABAY_KEY environment variable.

Repo state: `state/log.md` lists stories and Shorts already covered, so skip repeats. `state/python.json` holds the episode counter. To change the repo, first call add_repo(owner="koppalanaveenkumar", repo="bytewise-autopilot", access="push"), then commit with `git pull --rebase` and `git push` on main.

## 0. Setup (every run, fresh workspace)

```bash
git clone --depth 1 https://github.com/koppalanaveenkumar/bytewise-autopilot /tmp/bw
BW=/tmp/bw; bash $BW/setup.sh
W=/tmp/work; mkdir -p $W/out; cd $W
```

Each tool's first lines say how to use it.

## 1. Morning news (7 stories, about 2 minutes, ready by 7:00 IST)

1. **Research.** Search the web for the last 24-36 hours of tech and AI news. Pick 7 stories a beginner cares about. Prefer big names, money, safety, India relevance, and anything with strong visuals. Verify every number and claim in at least one reliable source. Anthropic stories: strictly factual, no opinion. No rumours stated as facts ("reports say" for unconfirmed deals).
2. **Script** (`el_script.txt`, one paragraph per story, blank line between):
   - Paragraph 1, the hook: ONE topic only. Use the most visual story in 1-2 short sentences. Then a bridge: "That's one of seven big tech stories for your <Weekday>."
   - Paragraphs 2-8: one story each, 3-5 short sentences, simple English, zero jargon.
   - Last paragraph: "Which story surprised you most? Tell me in the comments. And follow for simple tech news every morning."
   - No numbering anywhere: no "story one", no "comment one to seven".
   - First person singular only ("me", "I"), never "we"/"us".
   - Put pronunciation fixes in `say.json`, for example {"1859": "eighteen fifty-nine", "FAA": "F A A"}.
3. **Voice + timings:** `python3 $BW/tools/gen.py && python3 $BW/tools/export.py`
4. **Footage:**
   - `PIXABAY_KEY=... python3 $BW/tools/search.py "query" ...`. Use 2 queries per story, plus one for the hook and the ending.
   - Look at the `px/sheet_*.jpg` contact sheets.
   - Pick real, relevant clips. Never put an identifiable person next to accusatory text (hack, scam, cheat, fired). No branded logos you would have to draw.
   - Write `plan.json`. Segments cover 0 to the end of the voice timeline, 1-2 clips per story, with a montage of all stories during the hook's bridge sentence. Then run `python3 $BW/tools/bg.py`.
5. **Scenes:**
   - Copy `$BW/engine/example_news_scenes.js` to `$W/scenes.js` and rewrite `S[0]..S[8]` for today's stories. Keep `TILES` as short headline labels (no numbers), `header`, `hit(...)`, `footage()` and `renderAt` as they are.
   - Use `W("word", para)` to time visuals to the voice. A key visual must not start on a story's last word, and must stay 2+ seconds on screen.
   - Build: `python3 $BW/tools/build_page.py $W $W/scenes.js`
6. **HOOK CHECKLIST.** Check this on stills before the full render: `python3 $BW/tools/rec.py $W 8800 stills 0 1 2.5 4 6 ...` (one per story), then open `/tmp/nw_*.jpg` and look at them.
   - [ ] Frame 0 is full and something is already moving (real footage plus animation). No static text card, no date line, no story grid.
   - [ ] Opening text is 2 short lines at most.
   - [ ] The first 4-5 seconds are about ONE topic only.
   - [ ] No text overlaps, nothing cut off at the edges, captions readable.
   - [ ] No numbers or story counters on screen.
7. **Render:** `bash $BW/tools/render.sh $W $W/out/tech-news-<mon><dd>.mp4`. This takes about 25 minutes on 2 CPUs. Then spot-check 4 frames from the finished file.
8. **Thumbnail:**
   - Base it on `tools/thumbs_example.py`.
   - Use a REAL photo frame from one of today's clips, full-bleed, graded.
   - At most 3 big words, with a TOPIC tag pill, plus the logo badge.
   - Make 2 options for the two strongest stories and recommend one.
9. **Text to paste:**
   - YouTube title that matches the hook and the recommended thumbnail (no date).
   - Description: 2-line summary, then • bullets (no numbering), then "Follow for simple tech news every morning." and #technews #ai #shorts.
   - About 15 tags.
   - Instagram caption ending with: #explorepage #foryou #fyp #viralreels #trendingnow

## 2. Evening explainer Short (about 45-50 seconds, ready by 18:00 IST)

- Pick the hottest tech topic of the day; the user says yesterday's topic got more reach. Title format: "What is X? Explained Simply" (no date, no hashtags in the title).
- Script: hook in the first 2 seconds, one idea, simple English, 5-6 short paragraphs (one per scene). End with "Follow for more simple tech explained".
- Same engine and same steps (voice, footage, scenes, checklist, render). Use about 6 scenes, with the header text "EXPLAINED SIMPLY".
- Thumbnail rules are the same as the news.

## 3. Python for Beginners episodes (2 a day, Mon-Sat; slot A posts 18:00, slot B posts 19:00 IST)

1. **Claim the episode number first.** Pull main, read `state/python.json`, take `last_episode + 1` and the first item of `next_topics`. Write those back (`last_episode` +1, topic moved into `done`), then commit and push right away, so slot B gets the next one.
2. The title format is "Python for Beginners | Episode N - Explained Simply". The script follows the ByteWise long-video rules:
   - hook in the first 10 seconds
   - one concept at a time
   - one real-life example
   - a recap at the end
   - CTA: "Subscribe for Episode N+1 - simple tech explained"
   - aim for 2.5-4 minutes
   - "with me", never "us"
   Run every code example in Python first, so the screen output is real.
3. Kit: `$BW/python_episode/`. Copy `scenes_ep11.py` to `$W/scenes_epN.py` and rewrite `GROUPS` and the scenes for the topic, keeping the same look (1440p, code windows with typing, output panel, LEARN tag, chapter label).
   - Voice: `python3 $BW/tools/gen.py` in `$W`.
   - Check: `cd $W && SCENES=scenes_epN python3 $BW/python_episode/build_episode.py plan`, then `... frames <sceneid>:<t> ...` and look at `out/sheet.png`.
   - Render: `... render`, then `OUTNAME=$W/out/python-for-beginners-epN-<slug>.mp4 ... join`. This prints the chapters.
   - Subtitles: `python3 $BW/python_episode/srt.py $W/out/python-for-beginners-epN-english.srt`
4. Thumbnail: 1280x720, in the style of `python_episode/example_thumb_ep11.png` (EP N, 3 words or fewer, Python tag, logo). No cartoon characters.
5. Posting: YouTube only (horizontal video), slot A at 18:00 IST, slot B at 19:00 IST. The description includes the chapters.

## Style rules (all formats)

- Realistic: real stock footage behind everything, darkened at the top and bottom, plus motion graphics on top. No cartoon, anime or voxel characters. No drawn company logos.
- The logo badge is always at the top left. The first frame is always full.
- No music, no transition sounds.
- Don't name subjects like biology, commerce or arts.

## Delivering and posting (one-tap)

1. **Update the log.** Append today's news headlines (or the Short's topic) to `state/log.md`, then commit and push.
2. **Upload copy.** `bash $BW/tools/publish_prep.sh OUT.mp4 THUMB.png SLOT` with SLOT = news | short | epA | epB. It makes a high-quality copy under 100 MB on a public media branch and prints VIDEO_URL and THUMB_URL.
3. **Import into vidIQ.** `vidiq_video_upload(url=VIDEO_URL)` gives an uploadId. `vidiq_upload_image` with THUMB_URL gives a thumbnail image id; YouTube allows thumbnails under 2 MB, so shrink to JPEG if needed.
4. **Find the accounts.** `vidiq_social_account_list` gives the YouTube and Instagram account ids that have canPublish set.
5. **Create the draft.** `vidiq_social_post_draft_create` with media = the uploadId and publishAt = the slot time today in IST, e.g. 2026-11-24T08:00:00+05:30. Use the next day if that time has already passed.
   - **YOUTUBE** destination: title, text = description, tags, privacyStatus "public", thumbnailImageId.
   - **INSTAGRAM** destination: text = caption. News and Shorts only.
   - Fix anything the draft refuses with `vidiq_social_post_draft_update`.
6. **Notify the user.** Send the video file, the thumbnails and the text with SendUserFile and SendUserMessage, so their phone gets a notification. Say exactly when it will go out. End with: "Reply 'post it' to schedule it, or tell me what to change."
7. **Publish only on approval.**
   - Only after the user replies "post it" in this chat: `vidiq_social_post_publish(postId, revision)`. Then confirm the scheduled time and say whether any destination was refused.
   - If they ask for changes, make them, re-render if needed, and update the draft.
   - If they reply after the slot time, set publishAt to now plus 10 minutes and say so.

Slot times (IST): news 08:00 every day · Short 17:00 every day · Python A 18:00 and Python B 19:00, Mon-Sat.
