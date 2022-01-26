/*!
 * Theia Sticky Sidebar v1.3.0
 * https://github.com/WeCodePixels/theia-sticky-sidebar
 *
 * Glues your website's sidebars, making them permanently visible while scrolling.
 *
 * Copyright 2013-2014 WeCodePixels and other contributors
 * Released under the MIT license
 */
!function(i){"use strict";i.fn.theiaStickySidebar=function(t){(t=i.extend({containerSelector:"",additionalMarginTop:0,additionalMarginBottom:0,updateSidebarHeight:!0,minWidth:0,sidebarBehavior:"modern",wrap:"",exclude:".elementor-element-overlay, .ui-resizable-handle",active:!0},t)).additionalMarginTop=parseInt(t.additionalMarginTop)||0,t.additionalMarginBottom=parseInt(t.additionalMarginBottom)||0;var o=t.additionalMarginTop;function e(t,e){return!0===t.initialized||!(i("body").width()<t.minWidth)&&(function(t,e){t.initialized=!0,i("head").append(i('<style>.theiaStickySidebar:after {content: ""; display: table; clear: both;}</style>')),e.each((function(){var e={};e.sidebar=i(this),e.options=t||{},e.container=i(e.options.containerSelector),0==e.container.size()&&(e.container=e.sidebar.parent()),e.sidebar.parents().css("-webkit-transform","none"),e.sidebar.css({position:"relative",overflow:"visible","-webkit-box-sizing":"border-box","-moz-box-sizing":"border-box","box-sizing":"border-box"}),e.stickySidebar=e.sidebar.find(".theiaStickySidebar"),0==e.stickySidebar.length&&(e.sidebar.find("script").remove(),e.stickySidebar=i("<div>").addClass("theiaStickySidebar"),i(e.sidebar.children(t.wrap)).each((function(o,a){i(a).is(t.exclude)||e.stickySidebar.append(a)})),e.sidebar.append(i("<div>").addClass("jegStickyHolder").append(e.stickySidebar))),e.marginTop=parseInt(e.sidebar.css("margin-top")),e.marginBottom=parseInt(e.sidebar.css("margin-bottom")),e.paddingTop=parseInt(e.sidebar.css("padding-top")),e.paddingBottom=parseInt(e.sidebar.css("padding-bottom"));var a=e.stickySidebar.offset().top,n=e.stickySidebar.outerHeight();function d(){e.fixedScrollTop=0,e.sidebar.css({"min-height":"1px"}),e.stickySidebar.css({position:"static",width:""})}function r(t){var o=t.height();return t.children().each((function(){o=Math.max(o,i(this).height())})),o}e.stickySidebar.css("padding-top",1),e.stickySidebar.css("padding-bottom",1),a-=e.stickySidebar.offset().top,n=e.stickySidebar.outerHeight()-n-a,0==a?(e.stickySidebar.css("padding-top",0),e.stickySidebarPaddingTop=0):e.stickySidebarPaddingTop=1,0==n?(e.stickySidebar.css("padding-bottom",0),e.stickySidebarPaddingBottom=0):e.stickySidebarPaddingBottom=1,e.previousScrollTop=null,e.fixedScrollTop=0,d(),e.onScroll=function(o){if(t.active){if(!o.stickySidebar.is(":visible"))return;if(i("body").width()<o.options.minWidth)return void d();if(o.sidebar.outerWidth(!0)+50>o.container.width())return void d();var e=i(document).scrollTop(),a="static";if(e>=o.container.offset().top+(o.paddingTop+o.marginTop-o.options.additionalMarginTop)){var n,s=o.paddingTop+o.marginTop+t.additionalMarginTop,c=o.paddingBottom+o.marginBottom+t.additionalMarginBottom,p=o.container.offset().top,b=o.container.offset().top+r(o.container),l=0+t.additionalMarginTop;n=o.stickySidebar.outerHeight()+s+c<i(window).height()?l+o.stickySidebar.outerHeight():i(window).height()-o.marginBottom-o.paddingBottom-t.additionalMarginBottom;var g=p-e+o.paddingTop+o.marginTop,h=b-e-o.paddingBottom-o.marginBottom,f=o.stickySidebar.offset().top-e,S=o.previousScrollTop-e;"fixed"==o.stickySidebar.css("position")&&"modern"==o.options.sidebarBehavior&&(f+=S),"legacy"==o.options.sidebarBehavior&&(f=n-o.stickySidebar.outerHeight(),f=Math.max(f,n-o.stickySidebar.outerHeight())),f=S>0?Math.min(f,l):Math.max(f,n-o.stickySidebar.outerHeight()),f=Math.max(f,g),f=Math.min(f,h-o.stickySidebar.outerHeight());var u=o.container.height()==o.stickySidebar.outerHeight();a=(u||f!=l)&&(u||f!=n-o.stickySidebar.outerHeight())?e+f-o.sidebar.offset().top-o.paddingTop<=t.additionalMarginTop?"static":"absolute":"fixed"}}else a="static";if("fixed"==a)o.stickySidebar.css({position:"fixed",width:o.sidebar.width(),top:f,left:o.sidebar.offset().left+parseInt(o.sidebar.css("padding-left"))});else if("absolute"==a){var m={};"absolute"!=o.stickySidebar.css("position")&&(m.position="absolute",m.top=e+f-o.sidebar.offset().top-o.stickySidebarPaddingTop-o.stickySidebarPaddingBottom),m.width=o.sidebar.width(),m.left="",o.stickySidebar.css(m)}else"static"==a&&d();"static"!=a&&1==o.options.updateSidebarHeight&&o.sidebar.css({"min-height":o.stickySidebar.outerHeight()+o.stickySidebar.offset().top-o.sidebar.offset().top+o.paddingBottom}),o.previousScrollTop=e},e.onScroll(e),i(document).scroll(function(i){return function(){i.onScroll(i)}}(e)),i(window).resize(function(i){return function(){i.stickySidebar.css({position:"static"}),i.onScroll(i)}}(e)),i(window).bind("jnews_additional_sticky_margin",(function(i,a){t.additionalMarginTop=a+o,e.options.additionalMarginTop=a+o}))}))}(t,e),!0)}!function(t,o){e(t,o)||(console.log("TST: Body width smaller than options.minWidth. Init is delayed."),i(document).scroll(function(t,o){return function(a){e(t,o)&&i(this).unbind(a)}}(t,o)),i(window).resize(function(t,o){return function(a){e(t,o)&&i(this).unbind(a)}}(t,o)))}(t,this),i(this).bind("theiaStickySidebarDeactivate",(function(){t.active=!1})),i(this).bind("theiaStickySidebarActivate",(function(){t.active=!0}))}}(jQuery)