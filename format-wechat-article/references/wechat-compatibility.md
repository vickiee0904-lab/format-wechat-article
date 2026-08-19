# WeChat Compatibility

Create two separate documents: a pasteable article fragment and a browser preview wrapper.

## Article Fragment

- Put all presentation rules in `style` attributes on elements.
- Use common structural elements such as `section`, `p`, `span`, `strong`, `em`, `blockquote`, `ol`, `ul`, `li`, `img`, `br`, and simple tables only when essential.
- Do not include `script`, `style`, `link`, `iframe`, `form`, `input`, `button`, `video`, `audio`, `canvas`, `object`, or embedded interactive content.
- Do not rely on classes, ids, CSS variables, pseudo-elements, media queries, hover states, animations, sticky positioning, or external fonts.
- Prefer solid colors, borders, spacing, and restrained radius. Treat gradients and shadows as optional enhancement because editor sanitization can vary.
- Use explicit pixel-based font sizes and line heights. Avoid viewport units.
- Make every image responsive: `width:100%; max-width:100%; height:auto; display:block`.
- Add meaningful `alt` text. Keep captions as ordinary styled text below the image.
- Use tables sparingly; wide tables often overflow on phones.

## Images

- Local absolute paths are for preview only and are not publish-ready.
- For manual publishing, upload images in the公众号 editor and recheck their positions.
- For API publishing, upload assets through the platform's supported media flow and replace preview sources with returned URLs or media references.
- Do not use hotlinked images unless the user controls the host and has verified editor behavior.
- Preserve the original image aspect ratio unless a crop was explicitly approved.

## Preview Wrapper

The preview may include CSS, JavaScript, device chrome, copy controls, and diagnostics outside the article root. Never copy those elements into `article.html`.

## Final QA

1. Run the bundled validator.
2. Inspect at 375 px and a narrower Android viewport.
3. Verify title wrapping, paragraph rhythm, list indentation, quote borders, image width, and section spacing.
4. Paste into a disposable公众号 draft when available; compare hierarchy and image placement after sanitization.
5. Re-run factual/content preservation checks after any manual editor changes.

