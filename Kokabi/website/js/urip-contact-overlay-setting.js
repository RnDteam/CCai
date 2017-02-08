/* ==================================
	   Contact Overlay
	   (works with multiple buttons)
	=====================================*/
	var triggerBttn = document.querySelectorAll( '.contact-trigger' );

	var	overlay = document.querySelector( 'div.contact-overlay' ),
		closeBttn = overlay.querySelector( 'a.overlay-close' );
		transEndEventNames = {
			'WebkitTransition': 'webkitTransitionEnd',
			'MozTransition': 'transitionend',
			'OTransition': 'oTransitionEnd',
			'msTransition': 'MSTransitionEnd',
			'transition': 'transitionend'
		},
		transEndEventName = transEndEventNames[ Modernizr.prefixed( 'transition' ) ],
		support = { transitions : Modernizr.csstransitions };

	function toggleOverlay() {
		if( classie.has( overlay, 'open' ) ) {
			classie.remove( overlay, 'open' );
			classie.add( overlay, 'close' );
			$('body').removeClass('overlay-on');
			var onEndTransitionFn = function( ev ) {
				if( support.transitions ) {
					if( ev.propertyName !== 'visibility' ) return;
					this.removeEventListener( transEndEventName, onEndTransitionFn );
				}
				classie.remove( overlay, 'close' );
			};
			if( support.transitions ) {
				overlay.addEventListener( transEndEventName, onEndTransitionFn );
			}
			else {
				onEndTransitionFn();
			}
		}
		else if( !classie.has( overlay, 'close' ) ) {
			$("body").addClass('overlay-on');
			classie.add( overlay, 'open' );
		}
		classie.remove(overlay, 'close');
	}

	var i;
	for (i = 0; i < triggerBttn.length; i++) {
		triggerBttn[i].addEventListener( 'click', toggleOverlay );
	}
	closeBttn.addEventListener( 'click', toggleOverlay );