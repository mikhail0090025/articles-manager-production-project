// animations.js
(function(){
  const resultsRoot = document.getElementById("search_results");
  const searchBtn = document.getElementById("search_button");

  if (!resultsRoot) return;

  const onNewNode = (node) => {
    if (!(node instanceof HTMLElement)) return;

    // animate result cards
    if (node.classList && node.classList.contains("result-item")) {
      // ensure it is not already visible
      requestAnimationFrame(()=> {
        node.classList.add("enter");
        node.style.opacity = 1;
        node.addEventListener("animationend", () => {
          node.classList.remove("enter");
        }, { once: true });
      });
      // scroll newest into view (optional)
      node.scrollIntoView({ behavior: "smooth", block: "nearest" });
      return;
    }

    // animate plain <p> messages with "Error" or "No results"
    if (node.tagName === "P") {
      const text = node.textContent || "";
      if (/error|no results|not found/i.test(text)) {
        node.classList.add("error-anim");
        node.addEventListener("animationend", () => node.classList.remove("error-anim"), { once: true });
      } else {
        // fade in generic messages
        node.style.opacity = 0;
        node.classList.add("enter");
        node.addEventListener("animationend", () => node.classList.remove("enter"), { once: true });
      }
    }
  };

  const observer = new MutationObserver((mutations) => {
    for (const mut of mutations) {
      for (const added of mut.addedNodes) {
        if (added.nodeType !== Node.ELEMENT_NODE) continue;
        // if a container with many children was added, animate its children
        if (added.children && added.children.length > 0) {
          Array.from(added.children).forEach(child => onNewNode(child));
        } else {
          onNewNode(added);
        }
      }
    }
  });

  observer.observe(resultsRoot, { childList: true, subtree: false });

  // ripple effect on button (non-invasive)
  if (searchBtn) {
    searchBtn.addEventListener("click", function(e){
      const rect = this.getBoundingClientRect();
      const x = e.clientX - rect.left;
      const y = e.clientY - rect.top;
      const ripple = document.createElement("span");
      ripple.className = "ripple";
      ripple.style.width = ripple.style.height = Math.max(rect.width, rect.height) + "px";
      ripple.style.left = x + "px";
      ripple.style.top = y + "px";
      this.appendChild(ripple);
      // cleanup when animation done
      ripple.addEventListener("animationend", ()=> ripple.remove(), { once: true });
    });
  }

  // If there are already result items on load — animate them a bit
  Array.from(resultsRoot.children).forEach(child => {
    if (child.classList && child.classList.contains("result-item")) {
      child.style.opacity = 1;
    }
  });

})();
