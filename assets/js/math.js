// Render arithmatex output (\( … \) and \[ … \]) with the vendored KaTeX on every page load.
document$.subscribe(({ body }) => {
  if (typeof renderMathInElement !== "function") return;
  renderMathInElement(body, {
    delimiters: [
      { left: "$$", right: "$$", display: true },
      { left: "\\(", right: "\\)", display: false },
      { left: "\\[", right: "\\]", display: true },
    ],
    throwOnError: false,
  });
});
