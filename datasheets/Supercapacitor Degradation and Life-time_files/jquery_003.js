!function(e){"use strict";var a=!!("object"==typeof jnews&&"object"==typeof jnews.library)&&jnews.library,t=function(t,o){if(a){var n=this;n.element=e(t),n.options=o,n.xhr=null,n.xhr_cache=[],n.lock_action=!1,n.unique=n.element.data("unique"),n.data={filter:0,filter_type:"all",current_page:1,attribute:window[n.unique]||{}},n.ajax_mode=n.data.attribute.pagination_mode,n.header=n.element.find(".jeg_block_heading"),n.container=n.element.find(".jeg_block_container"),n.nav_block=n.element.find(".jeg_block_navigation"),n.ad_code=n.element.find(".jeg_ad_code").val(),n.nav_next=null,n.nav_prev=null,n.module_overlay=n.container.find(".module-overlay"),n.load_more_block=n.nav_block.find(".jeg_block_loadmore"),"nextprev"===n.ajax_mode&&(n.nav_next=n.nav_block.find(".next"),n.nav_prev=n.nav_block.find(".prev"),n.nav_next.on("click",e.proxy(n.click_next,n)),n.nav_prev.on("click",e.proxy(n.click_prev,n))),"loadmore"!==n.ajax_mode&&"scrollload"!==n.ajax_mode||(n.nav_next=n.load_more_block.find("a"),n.nav_next.on("click",e.proxy(n.load_more,n))),"scrollload"===n.ajax_mode&&(n.load_limit=n.data.attribute.pagination_scroll_limit,n.load_scroll()),n.masonry_init(),n.init(),n.element.trigger("jnews_module_init",[n])}};t.DEFAULTS={},t.prototype.init=function(){var e=this;e.subcat=e.header.find(".jeg_subcat"),e.subcat.length&&e.subcat.okayNav({swipe_enabled:!1,threshold:80,toggle_icon_content:"<span></span><span></span><span></span>"}),e.assign_header()},t.prototype.load_scroll=function(){var e=this;e.nav_next.hasClass("disabled")||(e.load_limit>e.data.current_page||0==e.load_limit)&&e.nav_next.waypoint((function(){e.data.current_page=e.data.current_page+1,e.request_ajax("scroll"),this.destroy()}),{offset:"100%",context:window})},t.prototype.click_next=function(a){var t=this,o=t.nav_next;a.preventDefault(),e(o).hasClass("disabled")||t.lock_action||(t.data.current_page=t.data.current_page+1,t.request_ajax("next"))},t.prototype.click_prev=function(a){var t=this,o=t.nav_prev;a.preventDefault(),e(o).hasClass("disabled")||t.lock_action||(t.data.current_page=t.data.current_page-1,t.request_ajax("prev"))},t.prototype.load_more=function(a){var t=this,o=t.nav_next;a.preventDefault(),e(o).hasClass("disabled")||t.lock_action||(t.data.current_page=t.data.current_page+1,t.request_ajax("more"))},t.prototype.assign_header=function(){var a=this;e(a.header).on("click",".subclass-filter",e.proxy(a.subclass_click,a))},t.prototype.subclass_click=function(a){var t=this,o=a.target;a.preventDefault(),t.lock_action||(this.header.find(".subclass-filter").removeClass("current"),e(o).addClass("current"),t.data.filter=e(o).data("id"),t.data.filter_type=e(o).data("type"),t.data.current_page=1,t.request_ajax("subclass"))},t.prototype.request_ajax=function(a){var t=this;t.lock_action=!0;var o={action:jnewsoption.module_prefix+t.data.attribute.class,module:!0,data:t.data},n=t.cache_get(o);n?(t.before_ajax_request(a,!1),setTimeout((function(){t.load_ajax(a,o,n),t.element.trigger("jnews_module_ajax")}),100)):(t.before_ajax_request(a,!0),t.xhr=e.ajax({url:jnews_ajax_url,type:"post",dataType:"json",data:o,success:function(e){t.load_ajax(a,o,e),t.cache_save(o,e),t.element.trigger("jnews_module_ajax")}}))},t.prototype.cache_get=function(e){for(var a=this,t=JSON.stringify(e),o=0;o<a.xhr_cache.length;o++)if(a.xhr_cache[o].param==t)return a.cache_prepare(a.xhr_cache[o].result);return!1},t.prototype.cache_prepare=function(a){a.content="<div>"+a.content+"</div>";var t=e(a.content);return t.find("img").each((function(){var a=e(this).data("src");e(this).attr("src",a).removeClass("lazyload").addClass("lazyloaded")})),a.content=t.html(),a},t.prototype.cache_save=function(e,a){var t=JSON.stringify(e);this.xhr_cache.push({param:t,result:a})},t.prototype.load_ajax=function(e,a,t){var o=this;switch(o.lock_action=!1,o.ajax_mode){case"loadmore":o.load_ajax_load_more(t,e);break;case"scrollload":o.load_scroll_more(t,e);break;default:o.load_ajax_next_prev(t,e)}jnews.like&&jnews.like.init(),jnews.share&&jnews.share.init()},t.prototype.before_ajax_request=function(e,a){var t=this;t.element.removeClass("loaded next prev more scroll subclass").addClass("loading"),"next"!==e&&"prev"!==e&&"subclass"!==e||!a||t.module_overlay.show(),"more"!==e&&"scroll"!==e||t.load_more_block.find("a").text(t.load_more_block.find("a").data("loading")).addClass("active")},t.prototype.after_ajax_request=function(e){var a=this;a.element.removeClass("loading").addClass("loaded").addClass(e),"next"!==e&&"prev"!==e&&"subclass"!==e||a.module_overlay.hide(),"more"!==e&&"scroll"!==e||(a.load_more_block.find("a").text(a.load_more_block.find("a").data("load")).removeClass("active"),void 0!==a.load_more_block.find("a").data("icon")&&a.load_more_block.find("a").html(a.load_more_block.find("a").html()+' <i class="fa '+a.load_more_block.find("a").data("icon")+'"></i>'))},t.prototype.replace_content=function(a){this.container.children().each((function(){e(this).hasClass("module-overlay")||e(this).remove()})),this.container.prepend(a)},t.prototype.load_ajax_next_prev=function(a,t){var o=this;o.replace_content(a.content),null!==o.nav_next&&(a.next?o.nav_next.removeClass("disabled"):o.nav_next.addClass("disabled")),null!==o.nav_prev&&(a.prev?o.nav_prev.removeClass("disabled"):o.nav_prev.addClass("disabled")),a.next||a.prev?null!==o.nav_prev&&o.nav_next.parent().removeClass("inactive"):null!==o.nav_next&&o.nav_next.parent().addClass("inactive"),o.after_ajax_request(t),o.masonry_init(),e(window).trigger("resize")},t.prototype.load_ajax_load_more=function(a,t){var o=this,n=e(a.content),r=0;n.each((function(){(e(this).hasClass("jeg_ad_module")&&o.ad_code&&e(this).find(".ads-wrapper").html(o.ad_code),e(this).hasClass("jeg_post"))?e(this).addClass("jeg_ajax_loaded anim_"+r):e(this).find(".jeg_post").each((function(){e(this).addClass("jeg_ajax_loaded anim_"+r),r++}));r++})),o.container.find(".jeg_post").removeClass("jeg_ajax_loaded"),o.container.find(".jeg_ad_module").removeClass("jeg_ajax_loaded"),1==o.data.current_page?o.replace_content(n):o.element.find(".jeg_load_more_flag").append(n),a.next?o.nav_next.removeClass("disabled"):o.nav_next.addClass("disabled"),o.after_ajax_request(t),o.masonry_load_more(n),e(window).trigger("resize")},t.prototype.load_scroll_more=function(a,t){var o=this,n=e(a.content),r=0;n.each((function(){e(this).hasClass("jeg_post")?e(this).addClass("jeg_ajax_loaded anim_"+r):e(this).find(".jeg_post").each((function(){e(this).addClass("jeg_ajax_loaded anim_"+r),r++}));r++})),o.container.find(".jeg_post").removeClass("jeg_ajax_loaded"),o.container.find(".jeg_ad_module").removeClass("jeg_ajax_loaded"),1==o.data.current_page?o.container.html("").html(n):o.element.find(".jeg_load_more_flag").append(n),a.next?o.nav_next.removeClass("disabled"):o.nav_next.addClass("disabled"),o.after_ajax_request(t),o.masonry_load_more(n),e(window).trigger("resize"),setTimeout((function(){o.load_scroll()}),500)},t.prototype.masonry_load_more=function(e){var a=this;a.container.find(".jeg_posts_masonry").length&&setTimeout((function(){a.masonry.isotope("appended",e)}),150)},t.prototype.masonry_init=function(){var a=this;a.container.find(".jeg_posts_masonry").length&&(setTimeout((function(){a.masonry=a.container.find(".jeg_posts_masonry .jeg_posts").isotope({itemSelector:".jeg_post",layoutMode:"masonry"}),a.masonry.imagesLoaded().progress((function(){a.masonry.isotope("layout")}))}),150),e(window).on("resize",(function(){setTimeout((function(){a.masonry.isotope("layout")}),1e3)})))};var o=e.fn.jmodule;e.fn.jmodule=function(a){return e(this).each((function(){var o=e(this),n=e.extend({},t.DEFAULTS,o.data(),"object"==typeof a&&a),r=o.data("jeg.module");r||o.data("jeg.module",r=new t(this,n))}))},e.fn.jmodule.Constructor=t,e.fn.jmodule.noConflict=function(){return e.fn.jmodule=o,this},e(".jeg_module_hook").jmodule()}(jQuery)