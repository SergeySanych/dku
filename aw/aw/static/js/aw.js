document.querySelectorAll('a[href^="http"]').forEach(link => {
    link.setAttribute("target", "_blank");
    link.setAttribute("rel", "nofollow noopener")
});