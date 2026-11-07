// Open external links (YouTube, papers) in a new tab so the reader keeps their place.
document$.subscribe(() => {
  document.querySelectorAll(".md-content a[href^='http']").forEach((a) => {
    a.target = "_blank";
    a.rel = "noopener";
  });
});
