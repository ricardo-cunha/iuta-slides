(function () {
  const expected = window.IUTA_SLIDE_ACCESS_TOKEN;
  const actual = new URLSearchParams(window.location.search).get("access");

  if (expected && actual === expected) return;

  document.documentElement.innerHTML = `
    <head><title>Access required · IUTA Slides</title></head>
    <body style="font-family:system-ui,sans-serif;max-width:42rem;margin:5rem auto;padding:0 1.5rem;color:#274560">
      <h1>Presentation link required</h1>
      <p>This slide deck is available through its private access link. Ask the owner for the current link.</p>
    </body>`;
})();
