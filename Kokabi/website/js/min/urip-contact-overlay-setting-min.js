function toggleOverlay(){if(classie.has(overlay,"open")){classie.remove(overlay,"open"),classie.add(overlay,"close"),$("body").removeClass("overlay-on");var e=function(n){if(support.transitions){if("visibility"!==n.propertyName)return;this.removeEventListener(transEndEventName,e)}classie.remove(overlay,"close")};support.transitions?overlay.addEventListener(transEndEventName,e):e()}else classie.has(overlay,"close")||($("body").addClass("overlay-on"),classie.add(overlay,"open"));classie.remove(overlay,"close")}var triggerBttn=document.querySelectorAll(".contact-trigger"),overlay=document.querySelector("div.contact-overlay"),closeBttn=overlay.querySelector("a.overlay-close");transEndEventNames={WebkitTransition:"webkitTransitionEnd",MozTransition:"transitionend",OTransition:"oTransitionEnd",msTransition:"MSTransitionEnd",transition:"transitionend"},transEndEventName=transEndEventNames[Modernizr.prefixed("transition")],support={transitions:Modernizr.csstransitions};var i;for(i=0;i<triggerBttn.length;i++)triggerBttn[i].addEventListener("click",toggleOverlay);closeBttn.addEventListener("click",toggleOverlay);