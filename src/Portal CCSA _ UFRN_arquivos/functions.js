/*global jQuery,google,G_vmlCanvasManager:false */

/* ==================================================

Custom jQuery functions.

================================================== */

(function(){
	
	// USE STRICT
	"use strict";
	
	/////////////////////////////////////////////
	// PAGE FUNCTIONS
	/////////////////////////////////////////////
	
	var page = {
		init: function () {
			
			var deviceAgent = navigator.userAgent.toLowerCase(),
				agentID = deviceAgent.match(/(iphone|ipod|ipad|android|iemobile)/);
			
			if (agentID) {
				jQuery('body').addClass("mobile-browser");
			}
			
			if(jQuery.browser.msie && (parseInt(jQuery.browser.version, 10) <= 9)) {
				jQuery('body').addClass("browser-ie");
			}
						
			// FITVIDS
			jQuery('.portfolio-items:not(.carousel-items),.blog-items:not(.carousel-items),article.type-portfolio,article.type-post,article.type-team,.wpb_video_widget,.infocus-item,.recent-posts').fitVids();
										
			// FOOTER BEAM ME UP LINK
			jQuery('.beam-me-up').on('click', 'a', function(e) {
				e.preventDefault();
				jQuery('body,html').animate({scrollTop: 0}, 800);
			});
		
		}
	};
	
	
	/////////////////////////////////////////////
	// HEADER
	/////////////////////////////////////////////
	
	var navSearch = jQuery('#nav-search').find('input'),
		navSearchLink = jQuery('.nav-search-link'),		
		miniHeader = jQuery('#mini-header'),
		miniHeaderSearch = jQuery('#mini-search').find('input'),
		miniHeaderSearchLink = jQuery('.mini-search-link');
		
	var header = {
		init: function() {
			
			header.miniHeaderInit();
			
			navSearchLink.on('click', function(e) {
				if (jQuery('#container').width() > 767 || jQuery('body').hasClass('responsive-fixed')) {
					e.preventDefault();
					navSearch.animate({
						opacity: 1,
						width: 140
					}, 200);
					navSearch.focus();
				}
			});
			
			navSearch.focus(function() {
				if (jQuery('#container').width() > 767 || jQuery('body').hasClass('responsive-fixed')) {
					navSearch.css('display', 'inline-block').animate({
						opacity: 1,
						width: 140
					}, 200);
				}
			});
					
			navSearch.blur(function() {
				if (jQuery('#container').width() > 767 || jQuery('body').hasClass('responsive-fixed')) {
					jQuery(this).animate({
						opacity: 0,
						width: 1
					}, 200);
					setTimeout(function() {
						navSearch.css('display', 'none');
					}, 300);
				}
			});
						
			miniHeaderSearchLink.on('click', function(e) {
				e.preventDefault();
				miniHeaderSearch.animate({
					opacity: 1,
					width: 140
				}, 200);
				miniHeaderSearch.focus();
			});
			
			miniHeaderSearch.focus(function() {
				jQuery(this).animate({
					opacity: 1,
					width: 140
				}, 200);
			});
					
			miniHeaderSearch.blur(function() {
				jQuery(this).animate({
					opacity: 0,
					width: 1
				}, 200);
			});
			
			jQuery(window).scroll(function() { 
				if ((jQuery(this).scrollTop() > 300) && !jQuery('body').hasClass('has-mini-header')) {
					header.miniHeaderShow();
				} else if ((jQuery(this).scrollTop() < 250) && jQuery('body').hasClass('has-mini-header')) {
					header.miniHeaderHide();
				}
			});
							
		},
		miniHeaderInit: function() {
			miniHeader.find('a[title="home"]').html('<i class="icon-home"></i>');
		},
		miniHeaderShow: function() {
			jQuery('body').addClass('has-mini-header');
			miniHeader.animate({
				"top": "0"
			}, 400);
		},
		miniHeaderHide: function() {
			jQuery('body').removeClass('has-mini-header');
			miniHeader.animate({
				"top": "-80"
			}, 400);
		}
	};
	
	
	/////////////////////////////////////////////
	// NAVIGATION
	/////////////////////////////////////////////
	
	var nav = {
		init: function() {
		
			// Add parent class to items with sub-menus
			jQuery("ul.sub-menu").parent().addClass('parent');
			
			// Enable hover dropdowns for window size above tablet width
			jQuery("nav").find(".menu li.parent").hoverIntent({
				over: function() {
					if (jQuery('#container').width() > 767 || jQuery('body').hasClass('responsive-fixed')) {
						
						// Setup menuLeft variable, with main menu value
						var subMenuWidth = jQuery(this).find('ul.sub-menu:first').outerWidth(true);
						var mainMenuItemWidth = jQuery(this).outerWidth(true);
						var menuLeft = '-' + (Math.round(subMenuWidth / 2) - Math.round(mainMenuItemWidth / 2)) + 'px';
						var menuContainer = jQuery(this).parent().parent().parent();
						
						// Check if this is the top bar menu
						if (menuContainer.hasClass("top-menu")) {
							if (menuContainer.parent().parent().parent().hasClass("top-bar-menu-right")) {
							menuLeft = "";
							} else {
							menuLeft = "-1px";
							}
						}
						
						// Check if second level dropdown
						if (jQuery(this).find('ul.sub-menu:first').parent().parent().hasClass("sub-menu")) {
							menuLeft = jQuery(this).find('ul.sub-menu:first').parent().parent().outerWidth(true) - 2;
						}
						
						jQuery(this).find('ul.sub-menu:first').css("left", menuLeft);
						jQuery(this).find('ul.sub-menu:first').css('opacity', 0).slideDown(300).animate({
							opacity: 1
						}, {
							queue: false, 
							duration: 300
						});
					}
				},
				out:function() {
					if (jQuery('#container').width() > 767 || jQuery('body').hasClass('responsive-fixed')) {
						jQuery(this).find('ul.sub-menu:first').slideUp(300);
						nav.hideNav(jQuery(this).find('ul.sub-menu:first'));
					}
				}
			});
	
	
			// Set the current page for each nav if exists
			var mobileNavToggle = jQuery('.show-menu');		
			mobileNavToggle.each(function() {
				var mobileMenu = jQuery(this).next('nav').find('ul.menu');
				var menuSelectedText = mobileMenu.find('.current-menu-item:last > a').text();
				if (menuSelectedText !== "") {
					jQuery(this).html(menuSelectedText + '<i class="icon-angle-down"></i>');
				}
			});

			// Toggle Mobile Nav show/hide			
			mobileNavToggle.on('click', function(e) {
				e.preventDefault();
				jQuery(this).next('nav').find('ul.menu').slideToggle(400);
			});
			
			jQuery(window).smartresize(function(){  
				if (jQuery('#container').width() > 767 || jQuery('body').hasClass('responsive-fixed')) {
					var menus = jQuery('nav').find('ul.menu');
					menus.each(function() {
						jQuery(this).css("display", "");
					});
				}
			});
			
			// Set current language to top bar item
			var currentLanguage = jQuery('.languages-menu-item').parent().find('.current-language span').text();
			if (currentLanguage !== "") {
			jQuery('.languages-menu-item').text(currentLanguage);
			}
			
		},
		hideNav: function(subnav) {
			setTimeout(function() {
				if (subnav.css("opacity") === "0") {
					subnav.css("display", "none");
				}
			}, 300);
		}
	};
	
	
	/////////////////////////////////////////////
	// FLEXSLIDER FUNCTION
	/////////////////////////////////////////////
	
	var flexSlider = {
		init: function() {
						
			jQuery('.item-slider').flexslider({
				animation: "slide",              //String: Select your animation type, "fade" or "slide"
				slideDirection: "horizontal",   //String: Select the sliding direction, "horizontal" or "vertical"
				slideshow: true,	//Boolean: Animate slider automatically
				slideshowSpeed: 6000,           //Integer: Set the speed of the slideshow cycling, in milliseconds
				animationDuration: 500,			//Integer: Set the speed of animations, in milliseconds
				smoothHeight: true,         
				directionNav: true,             //Boolean: Create navigation for previous/next navigation? (true/false)
				controlNav: true,               //Boolean: Create navigation for paging control of each clide? Note: Leave true for manualControls usage
				keyboardNav: false,              //Boolean: Allow slider navigating via keyboard left/right keys
				mousewheel: false,              //Boolean: Allow slider navigating via mousewheel
				prevText: "Prev",           //String: Set the text for the "previous" directionNav item
				nextText: "Next",               //String: Set the text for the "next" directionNav item
				pausePlay: true,               //Boolean: Create pause/play dynamic element
				pauseText: '',             //String: Set the text for the "pause" pausePlay item
				playText: '',               //String: Set the text for the "play" pausePlay item
				randomize: false,               //Boolean: Randomize slide order
				slideToStart: 0,                //Integer: The slide that the slider should start on. Array notation (0 = first slide)
				animationLoop: true,            //Boolean: Should the animation loop? If false, directionNav will received "disable" classes at either end
				pauseOnAction: true,            //Boolean: Pause the slideshow when interacting with control elements, highly recommended.
				pauseOnHover: false,            //Boolean: Pause the slideshow when hovering over slider, then resume when no longer hovering
				controlsContainer: "",          //Selector: Declare which container the navigation elements should be appended too. Default container is the flexSlider element. Example use would be ".flexslider-container", "#container", etc. If the given element is not found, the default action will be taken.
				manualControls: "",             //Selector: Declare custom control navigation. Example would be ".flex-control-nav li" or "#tabs-nav li img", etc. The number of elements in your controlNav should match the number of slides/tabs.
				start: function(){},            //Callback: function(slider) - Fires when the slider loads the first slide
				before: function(){},           //Callback: function(slider) - Fires asynchronously with each slider animation
				after: function(){},            //Callback: function(slider) - Fires after each slider animation completes
				end: function(){}               //Callback: function(slider) - Fires when the slider reaches the last slide (asynchronous)
			});
			jQuery('#swift-slider').flexslider({
				animation: "slide",              //String: Select your animation type, "fade" or "slide"
				slideDirection: "horizontal",   //String: Select the sliding direction, "horizontal" or "vertical"
				slideshow: false,	//Boolean: Animate slider automatically
				slideshowSpeed: 8000,           //Integer: Set the speed of the slideshow cycling, in milliseconds
				animationDuration: 600,         //Integer: Set the speed of animations, in milliseconds
				directionNav: true,             //Boolean: Create navigation for previous/next navigation? (true/false)
				controlNav: false,               //Boolean: Create navigation for paging control of each clide? Note: Leave true for manualControls usage
				keyboardNav: false,              //Boolean: Allow slider navigating via keyboard left/right keys
				mousewheel: false,              //Boolean: Allow slider navigating via mousewheel
				prevText: "Prev",           //String: Set the text for the "previous" directionNav item
				nextText: "Next",               //String: Set the text for the "next" directionNav item
				pausePlay: false,               //Boolean: Create pause/play dynamic element
				animationLoop: true,            //Boolean: Should the animation loop? If false, directionNav will received "disable" classes at either end
				pauseOnAction: true,            //Boolean: Pause the slideshow when interacting with control elements, highly recommended.
				pauseOnHover: true,
				start: function(postsSlider) {
					jQuery('.swift-slider-loading').fadeOut(200);
					postsSlider.slides.eq(postsSlider.currentSlide).addClass('flex-active-slide'); 
					if (postsSlider.slides.eq(postsSlider.currentSlide).has('.flex-caption-large')) {
						var chart = postsSlider.slides.eq(postsSlider.currentSlide).find('.fw-chart');
						if (jQuery('body').hasClass("browser-ie")) {
						chart = postsSlider.slides.eq(postsSlider.currentSlide).find('.chart');
						}
						chart.each( function() {
							var countValue = parseInt(jQuery(this).attr('data-count'), 10);
							jQuery(this).data('easyPieChart').update(80);
							jQuery(this).find('span').replaceWith("<span>0</span>");
							jQuery(this).find('span').animateNumber(countValue);
						});
					}
					postsSlider.slides.eq(postsSlider.currentSlide).find('.comment-chart:not(.fw-chart) span').replaceWith("<span>0</span>");
				},
				before: function(postsSlider) {
					if (postsSlider.slides.eq(postsSlider.currentSlide).has('.flex-caption-large')) {
						var chart = postsSlider.slides.eq(postsSlider.currentSlide).find('.fw-chart');
						if (jQuery('body').hasClass("browser-ie")) {
						chart = postsSlider.slides.eq(postsSlider.currentSlide).find('.chart');
						}
						chart.each( function() {
							jQuery(this).data('easyPieChart').update(0);
							jQuery(this).find('span').replaceWith("<span>0</span>");
						});
					}
					setTimeout( function() {
						postsSlider.slides.eq(postsSlider.currentSlide).addClass('flex-active-slide');
						if (postsSlider.slides.eq(postsSlider.currentSlide).has('.flex-caption-large')) {
							var chart = postsSlider.slides.eq(postsSlider.currentSlide).find('.fw-chart');
							if (jQuery('body').hasClass("browser-ie")) {
							chart = postsSlider.slides.eq(postsSlider.currentSlide).find('.chart');
							}
							chart.each( function() {
								var countValue = parseInt(jQuery(this).attr('data-count'), 10);
								jQuery(this).data('easyPieChart').update(80);
								jQuery(this).find('span').animateNumber(countValue);
							});
						}
					}, 1000);
				}
			});
			jQuery('.content-slider').each(function() {
				var sliderAnimation = jQuery(this).attr('data-animation');
				var autoplay = jQuery(this).attr('data-autoplay');
				autoplay = ((autoplay === "yes") ? true : false);
				
				jQuery(this).flexslider({
					animation: sliderAnimation,              //String: Select your animation type, "fade" or "slide"
					slideshow: autoplay,	//Boolean: Animate slider automatically
					slideshowSpeed: 6000,           //Integer: Set the speed of the slideshow cycling, in milliseconds
					animationDuration: 1000,			//Integer: Set the speed of animations, in milliseconds
					smoothHeight: true,         
					directionNav: true,             //Boolean: Create navigation for previous/next navigation? (true/false)
					controlNav: false               //Boolean: Create navigation for paging control of each clide? Note: Leave true for manualControls usage
				});
			});
						
			// LOAD THE LOVE-IT CHARTS
			jQuery('#swift-slider li').each( function() {
				jQuery(this).find('.chart').each( function() {
					jQuery(this).easyPieChart({
						animate: 1000,
						size: 70,
						barColor: jQuery(this).attr('data-barcolor'),
						trackColor: 'transparent',
						scaleColor: 'transparent'
					});
					jQuery(this).find('span').replaceWith("<span>0</span>");
				});
			});
			
			// CAPTION HOVER ADD/REMOVE CLASSES
			jQuery('#swift-slider li').hover(function() {
				jQuery(this).find('.flex-caption-details').removeClass('closing');
				jQuery(this).find('.flex-caption-details').addClass('open');
			}, function() {
				jQuery(this).find('.flex-caption-details').addClass('closing');
				jQuery(this).find('.flex-caption-details').removeClass('open');
			});
						
			// CAPTION TRANSITION LISTENERS
			jQuery('.caption-details-inner').on('transitionend webkitTransitionEnd oTransitionEnd otransitionend MSTransitionEnd', function() {
				var chart = jQuery(this).find('.chart');
				if (jQuery(this).parent().hasClass('closing')) {
					chart.each( function() {
						jQuery(this).data('easyPieChart').update(0);
						jQuery(this).find('span').replaceWith("<span>0</span>");
					});
					jQuery(this).parent().removeClass('closing');
				} else if (jQuery(this).parent().hasClass('open')) {
					chart.each( function() {
						var countValue = parseInt(jQuery(this).attr('data-count'), 10);
						jQuery(this).data('easyPieChart').update(80);
						jQuery(this).find('span').animateNumber(countValue);
					});
				}
			});
			
		},
		thumb: function() {
			jQuery('.thumb-slider').flexslider({
				animation: "fade",              //String: Select your animation type, "fade" or "slide"
				slideDirection: "horizontal",   //String: Select the sliding direction, "horizontal" or "vertical"
				slideshow: true,	//Boolean: Animate slider automatically
				slideshowSpeed: 6000,           //Integer: Set the speed of the slideshow cycling, in milliseconds
				animationDuration: 600,         //Integer: Set the speed of animations, in milliseconds
				directionNav: true,             //Boolean: Create navigation for previous/next navigation? (true/false)
				controlNav: false,               //Boolean: Create navigation for paging control of each clide? Note: Leave true for manualControls usage
				keyboardNav: false              //Boolean: Allow slider navigating via keyboard left/right keys
			});
		}
	};
	
	/////////////////////////////////////////////
	// PORTFOLIO
	/////////////////////////////////////////////
	
	var portfolioContainer = jQuery('.portfolio-wrap').find('.filterable-items');
	
	var portfolio = {
		init: function() {
			
			
			portfolio.standardSetup();
			
			// SET ITEM HEIGHTS
			portfolio.setItemHeight();
			
			// PORTFOLIO WINDOW RESIZE
			jQuery(window).smartresize(function(){  
					portfolio.windowResized();
			});
			
			// Enable filter options on when there are items from that skill
			jQuery('.filtering li').each( function() {
				var itemCount = 0;
				var filter = jQuery(this),
					filterName = jQuery(this).find('a').attr('class'),
					portfolioItems = jQuery(this).parent().parent().parent().next('.filterable-items');
				
				portfolioItems.find('li').each( function() {
					if ( jQuery(this).hasClass(filterName) ) {
						filter.addClass('has-items');
						itemCount++;
					}
				});
				
				if (jQuery(this).hasClass('all')) {
					itemCount = portfolioItems.children('li').length;
					jQuery(this).find('.item-count').text(itemCount);
				} else {
					jQuery(this).find('.item-count').text(itemCount);
				}
			});
	
			// filter items when filter link is clicked
			jQuery('.filtering li').on('click', 'a', function(e) {
				e.preventDefault();
				jQuery(this).parent().parent().find('li').removeClass('selected');
				jQuery(this).parent().addClass('selected');
				var selector = jQuery(this).attr('data-filter');
				var portfolioItems = jQuery(this).parent().parent().parent().parent().next('.filterable-items');
				portfolioItems.isotope({ filter: selector });
			});  
			
			jQuery('.filter-wrap > a').on('click', function(e) {
				e.preventDefault();
				jQuery(this).parent().find('.filter-slide-wrap').slideToggle();
			});
		},
		standardSetup: function() {
			portfolioContainer.isotope({
				animationEngine: 'best-available',
				animationOptions: {
					duration: 300,
					easing: 'easeInOutQuad',
					queue: false
				},
				resizable: true,
				layoutMode: 'fitRows'
			}), flexSlider.thumb(), portfolioContainer.isotope("reLayout");
		},
		setItemHeight: function() {
			if (!portfolioContainer.hasClass('single-column')) {
				portfolioContainer.children().css('min-height','0');
				portfolioContainer.equalHeights();
			}
		},
		windowResized: function() {
			if (!portfolioContainer.hasClass('single-column')) {
				portfolio.setItemHeight();
			}
		}
	};
	
	
	/////////////////////////////////////////////
	// BLOG
	/////////////////////////////////////////////
	
	var blogItems = jQuery('.blog-wrap').find('.blog-items'),
		masonryPagination = jQuery('.blog-wrap').find('.masonry-pagination');
	
	var blog = {
		init: function() {
		
			// BLOG ITEM SETUP
			if (blogItems.hasClass('masonry-items')) {
				jQuery('.masonry-items').fitVids();
				blog.masonrySetup();
				blogItems.imagesLoaded(function () {
					blogItems.animate({opacity: 1}, 800);
					masonryPagination.fadeIn(1000);
					blog.masonrySetup();
				}), flexSlider.thumb(), blogItems.isotope("reLayout");
				
				// BLOG WINDOW RESIZE
				jQuery(window).smartresize(function(){  
						blog.windowResized();
				});
			} else {
				flexSlider.thumb();
			}
			
			
			// BLOG AUX SLIDEOUT
			jQuery('.blog-slideout-trigger').on('click', function(e) {
				e.preventDefault();
				
				// VARIABLES
				var blogWrap = jQuery(this).parent().parent().parent().parent();
				var filterPanel = blogWrap.find('.filter-wrap .filter-slide-wrap');
				var auxType = jQuery(this).attr('data-aux');
								
				// ADD COLUMN SIZE AND REMOVE BRACKETS FROM COUNT
				blogWrap.find('.aux-list li').addClass('span2');
				blogWrap.find('.aux-list li a span').each(function() {
					jQuery(this).html(jQuery(this).html().replace("(","").replace(")",""));
				});
				
				// IF SELECTING AN OPTION THAT IS OPEN, CLOSE THE PANEL
				if (jQuery(this).parent().hasClass('selected') && !filterPanel.is(':animated')) {
					blogWrap.find('.blog-aux-options li').removeClass('selected');
					filterPanel.slideUp(400);
					return;
				}
				
				// AUX BUTTON SELECTED STATE
				blogWrap.find('.blog-aux-options li').removeClass('selected');	
				jQuery(this).parent().addClass('selected');
				
				// IF SLIDEOUT IS OPEN
				if (filterPanel.is(':visible')) {
					
					filterPanel.slideUp(400);
					setTimeout(function() {
						blogWrap.find('.aux-list').css('display', 'none');
						blogWrap.find('.aux-'+auxType).css('display', 'block');
						filterPanel.slideDown();
					}, 600);
					
				// IF SLIDEOUT IS CLOSED
				} else {
					
					blogWrap.find('.aux-list').css('display', 'none');
					blogWrap.find('.aux-'+auxType).css('display', 'block');
					filterPanel.slideDown();
					
				}
			});
			
		},
		masonrySetup: function() {
			blogItems.isotope({
				itemSelector : '.blog-item',
				masonry : {
					columnWidth : 0
				},
				animationEngine: 'best-available',
				animationOptions: {
					duration: 300,
					easing: 'easeInOutQuad',
					queue: false
				},
				transformsEnabled: false,
				resizable: true
			});
		},
		windowResized: function() {
			blogItems.isotope("reLayout");
		}	
	};
	
	
	/////////////////////////////////////////////
	// CAROUSEL FUNCTIONS
	/////////////////////////////////////////////
	
	var carouselWidgets = {
		init: function() {
	
			// CAROUSELS
			var carousel = jQuery('.carousel-items');
			
			carousel.each(function() {
				var carouselInstance = jQuery('#'+jQuery(this).attr('id'));
				var carouselPrev = carouselInstance.parent().find('.prev');
				var carouselNext = carouselInstance.parent().find('.next');
				var carouselColumns = parseInt(carouselInstance.attr("data-columns"), 10);
				
				carouselInstance.imagesLoaded(function () {
					jQuery(this).carouFredSel({
						items				: carouselColumns,
						scroll : {
							items			: 1,
							easing			: "easeOutQuart",
							duration		: 1000,							
							pauseOnHover	: true
						},
						auto : {
							play			: false
						},
						prev : {	
							button			: carouselPrev,
							key				: "left"
						},
						next : { 
							button			: carouselNext,
							key				: "right"
						},
						onCreate : function() {
							jQuery(this).fadeIn(400, function() {
								jQuery(this).fitVids();
							});
							flexSlider.thumb();
							carouselWidgets.resizeCarousels();
						}	
					});
				});
			});
			
			jQuery(window).smartresize(function() {
				var carousel = jQuery('.carousel-items');
				carousel.trigger("updateSizes");
			});
		},
		resizeCarousels: function() {
			var carousel = jQuery('.carousel-items');
			
			jQuery(window).smartresize(function() {
				carousel.each(function() {
					var carouselItem = jQuery(this).find('.carousel-item');
					var itemWidth = carouselItem.width() + carouselItem.css('margin-left');
					
					carousel.trigger("configuration", {
						items : {
							width : itemWidth
						}				
					});
					
					if (carousel.is(':visible')) {
						if (jQuery(this).parent().hasClass('caroufredsel_wrapper')) {
							jQuery(this).parent().css('height', jQuery(this).children().first().outerHeight(true) + 1 + 'px');
						}
					}
				});
			}).trigger('resize');
		}
	};
	
	
	/////////////////////////////////////////////
	// WIDGET FUNCTIONS
	/////////////////////////////////////////////
	
	var widgets = {
		init: function() {
			
			// CHARTS
			if (sfIncluded.hasClass('has-chart')) {
				jQuery('.chart-shortcode').each(function(){
					jQuery(this).easyPieChart({
						animate: 1000,
						lineCap: 'square',
						lineWidth: jQuery(this).attr('data-linewidth'),
						size: jQuery(this).attr('data-size'),
						barColor: jQuery(this).attr('data-barcolor'),
						trackColor: jQuery(this).attr('data-trackcolor'),
						scaleColor: 'transparent'
					});
				});
			}
			
			// ASSET EQUAL HEIGHTS
			jQuery('.team-members').equalHeights();
			
			// RESIZE ASSETS
			widgets.resizeAssets();
			jQuery(window).smartresize(function() {  
				widgets.resizeAssets();
			});
			
			// SF TOOLTIPS
			jQuery('[rel=tooltip]').tooltip();
			
		},
		resizeAssets: function() {	
			var carousels = jQuery('.carousel-items');
			var assets = jQuery('.alt-bg');
			var assetWidth = 0;
			
			if (jQuery('#container').width() < 460 && jQuery('body').hasClass('responsive-fluid')) {
				assetWidth = jQuery('#container').width() - 40;			
				carousels.find('.carousel-item').each(function() {
					jQuery(this).css("width", assetWidth + "px");
					
				});
			} else if (jQuery('#container').width() < 768 && jQuery('body').hasClass('responsive-fluid')) {
				if (carousels.hasClass('testimonials')) {
				assetWidth = jQuery('#container').width() - 40;	
				} else {
				assetWidth = Math.floor(jQuery('#container').width() / 2) - 35;	
				}
				carousels.find('.carousel-item').each(function() {
					jQuery(this).css("width", assetWidth + "px");
				});
			} else if (jQuery('body').hasClass('responsive-fluid')) {
				carousels.find('.carousel-item').each(function() {
					jQuery(this).css("width", "");
				});
			}
			
			if (jQuery('#container').width() < 768 && jQuery('body').hasClass('responsive-fluid')) {
				assetWidth = jQuery('#container').width();
				assets.each(function() {
					jQuery(this).css("width", assetWidth + "px");
				});	
			} else {
				assets.each(function() {
					jQuery(this).css("width", "");
				});	
			}
		},
		initSkillBars: function() {		
			// SKILL BARS
			widgets.animateSkillBars();			
			jQuery(window).scroll(function() { 
				widgets.animateSkillBars();
			});
		},
		animateSkillBars: function() {
			jQuery('.progress:in-viewport').each(function(){
				var progressBar = jQuery(this),
				progressValue = progressBar.find('.bar').attr('data-value');
				if (!progressBar.hasClass('animated')) {
					progressBar.addClass('animated');
					progressBar.find('.bar').animate({
						width: progressValue + "%"
					}, 600, function() {
						progressBar.find('.bar-text').fadeIn(400);
					});
				}
			});
		},
		charts: function() {
			widgets.animateCharts();
			jQuery(window).scroll(function() { 
				widgets.animateCharts();
			});	
		},
		animateCharts: function() {
			jQuery('.chart-shortcode:in-viewport').each(function(){
				if (!jQuery(this).hasClass('animated')) {
					jQuery(this).addClass('animated');
					var animatePercentage = parseInt(jQuery(this).attr('data-animatepercent'), 10);
					jQuery(this).data('easyPieChart').update(animatePercentage);
				}
			});
		}
	};
	
	
	/////////////////////////////////////////////
	// PRETTYPHOTO FUNCTION
	/////////////////////////////////////////////
	
	var prettyPhoto = {
		init: function() {
			jQuery("a[rel^='prettyPhoto']").prettyPhoto({
				//theme: 'light_square'
			});
		}
	};
	
	
	/////////////////////////////////////////////
	// MAP FUNCTIONS
	/////////////////////////////////////////////
	
	var map = {
		init:function() {
			
			var maps = jQuery('.map-canvas');
			maps.each(function(index, element) {
				var mapContainer = element,
					mapAddress = mapContainer.getAttribute('data-address'),
					mapLat = mapContainer.getAttribute('data-lat'),
					mapLong = mapContainer.getAttribute('data-long'),
					mapZoom = mapContainer.getAttribute('data-zoom'),
					mapType = mapContainer.getAttribute('data-maptype'),
					pinLogoURL = mapContainer.getAttribute('data-pinimage'),
					mapTypeIdentifier = "";
				
				if (mapType === "satellite") {
				mapTypeIdentifier = google.maps.MapTypeId.SATELLITE;
				} else if (mapType === "terrain") {
				mapTypeIdentifier = google.maps.MapTypeId.TERRAIN;
				} else if (mapType === "hybrid") {
				mapTypeIdentifier = google.maps.MapTypeId.HYBRID;
				} else {
				mapTypeIdentifier = google.maps.MapTypeId.ROADMAP;
				}
						
				var latlng = new google.maps.LatLng(mapLat, mapLong);
				var settings = {
					zoom: parseInt(mapZoom, 10),
					scrollwheel: false,
					center: latlng,
					mapTypeControl: true,
					mapTypeControlOptions: {style: google.maps.MapTypeControlStyle.DROPDOWN_MENU},
					navigationControl: true,
					navigationControlOptions: {style: google.maps.NavigationControlStyle.SMALL},
					mapTypeId: mapTypeIdentifier
				};
				var mapInstance = new google.maps.Map(mapContainer, settings);
				var companyPos = "";
				var companyMarker = "";
				if (pinLogoURL) {
				var companyLogo = new google.maps.MarkerImage(pinLogoURL,
					new google.maps.Size(150,75),
					new google.maps.Point(0,0),
					new google.maps.Point(75,75)
				);
					companyPos = new google.maps.LatLng(mapLat, mapLong);
					companyMarker = new google.maps.Marker({
					position: companyPos,
					map: mapInstance,
					icon: companyLogo
				});
				} else { 
					companyPos = new google.maps.LatLng(mapLat, mapLong);
					companyMarker = new google.maps.Marker({
					position: companyPos,
					map: mapInstance
				});
				}
				google.maps.event.addListener(companyMarker, 'click', function() {
					window.location.href = 'http://maps.google.com/maps?q='+mapAddress;
				});
				
				google.maps.event.addDomListener(window, 'resize', function() {
					mapInstance.setCenter(companyPos);
				});
			});
			
			map.fullscreenMap();
			jQuery(window).smartresize(function(){
				map.fullscreenMap();
			});
			
		},
		fullscreenMap: function() {
			var fullscreenMap = jQuery('.fullscreen-map'),
				container = jQuery('#page-wrap'),
				mapOffset = container.offset().left,
				windowWidth = jQuery(window).width();

			if (windowWidth > 768) {
				mapOffset = mapOffset;
			} else {
				mapOffset = 20;
			}
						
			fullscreenMap.find('.map-canvas').css('width', windowWidth);
			fullscreenMap.css('margin-left', '-' + mapOffset + 'px');
			
		}
	};
	
	
	/////////////////////////////////////////////
	// NAV ARROW INDICATOR FUNCTION
	/////////////////////////////////////////////
	
	var navArrow = {
		init:function() {
			var navSection = jQuery("#nav-section");
			var mainNav = jQuery("#main-navigation");    
			mainNav.append("<div id='nav-pointer'></div>");
			var magicLine = jQuery("#nav-pointer");
			var currentMenuItem	= mainNav.find('>div>ul>.current-menu-item, >div>ul>.current_page_item');
			if(!currentMenuItem.length){ currentMenuItem = mainNav.find('.current-menu-ancestor:eq(0), .current_page_ancestor:eq(0)'); }
			
			if (navSection.hasClass('nav-indicator') && currentMenuItem.length > 0) {
				
				magicLine
					.width(currentMenuItem.find('a').width())
					.css("left", currentMenuItem.position().left + parseInt(currentMenuItem.find('a').css("margin-left"), 10))
					.data("origLeft", magicLine.position().left);
				
				var originalWidth = currentMenuItem.find('a').width();
					
				jQuery("#main-navigation > div > ul > li").hover(function() {
					var hoverMenuItem = jQuery(this).find('a');
					var leftPos = hoverMenuItem.parent().position().left + parseInt(hoverMenuItem.css("margin-left"), 10);
					var newWidth = hoverMenuItem.width();
					magicLine.stop().animate({
						left: leftPos,
						width: newWidth
					});
				}, function() {
					magicLine.stop().animate({
						left: magicLine.data("origLeft"),
						width: originalWidth
					});    
				});
			
			} else {
			
				magicLine.hide();
			
			}
		}
	};
	
	
	/////////////////////////////////////////////
	// RELOAD FUNCTIONS
	/////////////////////////////////////////////
	
	var reloadFunctions = {
		init:function() {	
			
			var deviceAgent = navigator.userAgent.toLowerCase(),
				appleAgentID = deviceAgent.match(/(iphone|ipod|ipad)/);
	
			// Remove title attributes from images to avoid showing on hover 
			jQuery('img[title]').each(function() {
				jQuery(this).removeAttr('title');
			});
			
			jQuery('.ui-tabs-nav').on('click', 'a', function() {
				jQuery(this).blur();
			});
			
			if (!appleAgentID) {
				jQuery('embed').show();
			}
						
			// Animate Top Links
			jQuery('.animate-top').on('click', function(e) {
				e.preventDefault();
				jQuery('body,html').animate({scrollTop: 0}, 800);           
			});
		},
		load:function() {
			var deviceAgent = navigator.userAgent.toLowerCase(),
				agentID = deviceAgent.match(/(iphone|ipod|ipad|android|iemobile)/);
				
			if (!agentID) {
			
				// Button hover tooltips
				jQuery('.tooltip').each( function() {
					jQuery(this).css( 'marginLeft', '-' + Math.round( (jQuery(this).outerWidth(true) / 2) ) + 'px' );
				});
				
				jQuery('.comment-avatar').hover( function() {
					jQuery(this).find('.tooltip' ).stop().animate({
						bottom: '44px',
						opacity: 1
					}, 500, 'easeInOutExpo');
				}, function() {
						jQuery(this).find('.tooltip').stop().animate({
							bottom: '25px',
							opacity: 0
						}, 400, 'easeInOutExpo');
				});
				
				jQuery('.grid-image').hover( function() {
					jQuery(this).find('.tooltip' ).stop().animate({
						bottom: '85px',
						opacity: 1
					}, 500, 'easeInOutExpo');
				}, function() {
						jQuery(this).find('.tooltip').stop().animate({
							bottom: '65px',
							opacity: 0
						}, 400, 'easeInOutExpo');
				});
			
			}	
		}
	};
	
	
	/////////////////////////////////////////////
	// LOAD + READY FUNCTION
	/////////////////////////////////////////////
	
	var sfIncluded = jQuery('#sf-included');
	
	var onReady = {
		init: function(){
			page.init();
			header.init();
			nav.init();
			widgets.init();
			prettyPhoto.init();
			if (sfIncluded.hasClass('has-carousel')) {
			carouselWidgets.init();
			}
			if (sfIncluded.hasClass('has-map')) {
			map.init();
			}
			reloadFunctions.init();
		}
	};
	var onLoad = {
		init: function(){
			flexSlider.init();
			if (sfIncluded.hasClass('has-portfolio')) {
			portfolio.init();
			}
			if (sfIncluded.hasClass('has-blog')) {
			blog.init();
			}
			navArrow.init();
			if (sfIncluded.hasClass('has-chart')) {
				widgets.charts();
			}
			if (sfIncluded.hasClass('has-progress-bar')) {
				widgets.initSkillBars();
			}
			reloadFunctions.load();
		}
	};
	
	jQuery(document).ready(onReady.init);
	jQuery(window).load(onLoad.init);
	
})(jQuery);

/////////////////////////////////////////////
// SMARTRESIZE PLUGIN
/////////////////////////////////////////////

(function($,sr){

	// USE STRICT
	"use strict";
	
	// debouncing function from John Hann
	// http://unscriptable.com/index.php/2009/03/20/debouncing-javascript-methods/
	var debounce = function (func, threshold, execAsap) {
		var timeout;
		
		return function debounced () {
			var obj = this, args = arguments;
			function delayed () {
				if (!execAsap) {
					func.apply(obj, args);
					timeout = null;
				}
			}
			
			if (timeout) {
				clearTimeout(timeout);
			} else if (execAsap) {
				func.apply(obj, args);
			}
			
			timeout = setTimeout(delayed, threshold || 100); 
		};
	};
	
	// smartresize 
	jQuery.fn[sr] = function(fn){  return fn ? this.bind('resize', debounce(fn)) : this.trigger(sr); };
 
})(jQuery,'smartresize');


/////////////////////////////////////////////
// EQUALHEIGHTS PLUGIN
/////////////////////////////////////////////

(function($) {

	// USE STRICT
	"use strict";
	
	$.fn.equalHeights = function(px) {
		$(this).each(function(){
			var currentTallest = 0;
			$(this).children().each(function(){
				if ($(this).height() > currentTallest) { currentTallest = $(this).height(); }
			});
			if (!px && Number.prototype.pxToEm) {
				currentTallest = currentTallest.pxToEm(); //use ems unless px is specified
			}
			// for ie6, set height since min-height isn't supported
			if ($.browser.msie && $.browser.version === 6.0) {
				(this).children().css({'height': currentTallest});
			}
			$(this).children().css({'min-height': currentTallest}); 
		});
		return this;
	};
})(jQuery);


/////////////////////////////////////////////
// EASYPIECHART PLUGIN
/////////////////////////////////////////////

(function($) {
	// USE STRICT
	"use strict";
	$.easyPieChart = function(el, options) {
		var addScaleLine, animateLine, drawLine, easeInOutQuad, renderBackground, renderScale, renderTrack,
		_this = this;
		this.el = el;
		this.$el = $(el);
		this.$el.data("easyPieChart", this);
		this.init = function() {
			var percent;
			_this.options = $.extend({}, $.easyPieChart.defaultOptions, options);
			percent = parseInt(_this.$el.data('percent'), 10);
			_this.percentage = 0;
			_this.canvas = $("<canvas width='" + _this.options.size + "' height='" + _this.options.size + "'></canvas>").get(0);
			_this.$el.append(_this.canvas);
			if (typeof G_vmlCanvasManager !== "undefined" && G_vmlCanvasManager !== null) {
				G_vmlCanvasManager.initElement(_this.canvas);
			}
			_this.ctx = _this.canvas.getContext('2d');
			if (window.devicePixelRatio > 1.5) {
				$(_this.canvas).css({
					width: _this.options.size,
					height: _this.options.size
				});
				_this.canvas.width *= 2;
				_this.canvas.height *= 2;
				_this.ctx.scale(2, 2);
			}
			_this.ctx.translate(_this.options.size / 2, _this.options.size / 2);
			_this.$el.addClass('easyPieChart');
			_this.$el.css({
				width: _this.options.size,
				height: _this.options.size,
				lineHeight: "" + _this.options.size + "px"
			});			
			_this.update(percent);
			return _this;
		};
		this.update = function(percent) {
			if (_this.options.animate === false) {
				return drawLine(percent);
			} else {
				if (percent === 0) {
					return animateLine(0, 0);	
				} else {
					return animateLine(_this.percentage, percent);	
				}
			}
		};
		renderScale = function() {
			var i, _i, _results;
			_this.ctx.fillStyle = _this.options.scaleColor;
			_this.ctx.lineWidth = 1;
			_results = [];
			for (i = _i = 0; _i <= 24; i = ++_i) {
				_results.push(addScaleLine(i));
			}
			return _results;
		};
		addScaleLine = function(i) {
			var offset;
			offset = i % 6 === 0 ? 0 : _this.options.size * 0.017;
			_this.ctx.save();
			_this.ctx.rotate(i * Math.PI / 12);
			_this.ctx.fillRect(_this.options.size / 2 - offset, 0, -_this.options.size * 0.05 + offset, 1);
			return _this.ctx.restore();
		};
		renderTrack = function() {
			var offset;
			offset = _this.options.size / 2 - _this.options.lineWidth / 2;
			if (_this.options.scaleColor !== false) {
				offset -= _this.options.size * 0.08;
			}
			_this.ctx.beginPath();
			_this.ctx.arc(0, 0, offset, 0, Math.PI * 2, true);
			_this.ctx.closePath();
			_this.ctx.strokeStyle = _this.options.trackColor;
			_this.ctx.lineWidth = _this.options.lineWidth;
			return _this.ctx.stroke();
		};
		renderBackground = function() {
			if (_this.options.scaleColor !== false) {
				renderScale();
			}
			if (_this.options.trackColor !== false) {
				return renderTrack();
			}
		};
		drawLine = function(percent) {
			var offset;
			renderBackground();
			_this.ctx.strokeStyle = $.isFunction(_this.options.barColor) ? _this.options.barColor(percent) : _this.options.barColor;
			_this.ctx.lineCap = _this.options.lineCap;
			_this.ctx.lineWidth = _this.options.lineWidth;
			offset = _this.options.size / 2 - _this.options.lineWidth / 2;
			if (_this.options.scaleColor !== false) {
				offset -= _this.options.size * 0.08;
			}
			_this.ctx.save();
			_this.ctx.rotate(-Math.PI / 2);
			_this.ctx.beginPath();
			_this.ctx.arc(0, 0, offset, 0, Math.PI * 2 * percent / 100, false);
			_this.ctx.stroke();
			return _this.ctx.restore();
		};
		animateLine = function(from, to) {
			var currentStep, fps, steps;
			fps = 30;
			steps = fps * _this.options.animate / 1000;
			currentStep = 0;
			_this.options.onStart.call(_this);
			_this.percentage = to;
			if (_this.animation) {
				clearInterval(_this.animation);
				_this.animation = false;
			}
			_this.animation = setInterval(function() {
				_this.ctx.clearRect(-_this.options.size / 2, -_this.options.size / 2, _this.options.size, _this.options.size);
				renderBackground.call(_this);
				drawLine.call(_this, [easeInOutQuad(currentStep, from, to - from, steps)]);
				currentStep++;
				if ((currentStep / steps) > 1) {
					clearInterval(_this.animation);
					_this.animation = false;
					return _this.options.onStop.call(_this);
				}
			}, 1000 / fps);
			return _this.animation;
		};
		easeInOutQuad = function(t, b, c, d) {
			var easeIn, easing;
			easeIn = function(t) {
				return Math.pow(t, 2);
			};
			easing = function(t) {
				if (t < 1) {
					return easeIn(t);
				} else {
					return 2 - easeIn((t / 2) * -2 + 2);
				}
			};
			t /= d / 2;
			return c / 2 * easing(t) + b;
		};
		return this.init();
	};
	$.easyPieChart.defaultOptions = {
		barColor: '#ef1e25',
		trackColor: '#f2f2f2',
		scaleColor: '#dfe0e0',
		lineCap: 'round',
		size: 110,
		lineWidth: 3,
		animate: false,
		onStart: $.noop,
		onStop: $.noop
	};
	$.fn.easyPieChart = function(options) {
		return $.each(this, function(i, el) {
		var $el;
		$el = $(el);
		if (!$el.data('easyPieChart')) {
			return $el.data('easyPieChart', new $.easyPieChart(el, options));
		}
		});
	};
	return void 0;
})(jQuery);


/////////////////////////////////////////////
// ANIMATE NUMBER PLUGIN
/////////////////////////////////////////////

(function($) {
	
	// USE STRICT
	"use strict";
	
    $.fn.animateNumber = function(to) {
        var $ele = $(this),
            num = parseInt($ele.html(), 10),
            up = to > num,
            num_interval = Math.abs(num - to) / 90;

        var loop = function() {
            num = up ? Math.ceil(num+num_interval) : Math.floor(num-num_interval);
            if ( (up && num > to) || (!up && num < to) ) {
                num = to;
                clearInterval(animation);
            }
            $ele.html(num);
        };
        
        var intervalTime = to <= 5 ? intervalTime = 100 : to <= 25 ? intervalTime = 50 : to <= 50 ? intervalTime = 25 : 10;

        var animation = setInterval(loop, intervalTime);
    };
})(jQuery);


/////////////////////////////////////////////
// VIEWPORT PLUGIN
/////////////////////////////////////////////

/*
 * Viewport - jQuery selectors for finding elements in viewport
 *
 * Copyright (c) 2008-2009 Mika Tuupola
 *
 * Licensed under the MIT license:
 *   http://www.opensource.org/licenses/mit-license.php
 *
 * Project home:
 *  http://www.appelsiini.net/projects/viewport
 *
 */


(function($) {

	// USE STRICT
	"use strict";
    
    $.belowthefold = function(element, settings) {
        var fold = $(window).height() + $(window).scrollTop();
        return fold <= $(element).offset().top - settings.threshold;
    };

    $.abovethetop = function(element, settings) {
        var top = $(window).scrollTop();
        return top >= $(element).offset().top + $(element).height() - settings.threshold;
    };
    
    $.rightofscreen = function(element, settings) {
        var fold = $(window).width() + $(window).scrollLeft();
        return fold <= $(element).offset().left - settings.threshold;
    };
    
    $.leftofscreen = function(element, settings) {
        var left = $(window).scrollLeft();
        return left >= $(element).offset().left + $(element).width() - settings.threshold;
    };
    
    $.inviewport = function(element, settings) {
        return !$.rightofscreen(element, settings) && !$.leftofscreen(element, settings) && !$.belowthefold(element, settings) && !$.abovethetop(element, settings);
    };
    
    $.extend($.expr[':'], {
        "below-the-fold": function(a) {
            return $.belowthefold(a, {threshold : 0});
        },
        "above-the-top": function(a) {
            return $.abovethetop(a, {threshold : 0});
        },
        "left-of-screen": function(a) {
            return $.leftofscreen(a, {threshold : 0});
        },
        "right-of-screen": function(a) {
            return $.rightofscreen(a, {threshold : 0});
        },
        "in-viewport": function(a) {
            return $.inviewport(a, {threshold : 0});
        }
    });

    
})(jQuery);