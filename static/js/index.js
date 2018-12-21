import $ from 'jquery';
import jQuery from 'jquery';

import 'owl.carousel';
import 'lightgallery/src/sass/lightgallery.scss';
import '../scss/index.scss';
// require('vimeo-froogaloop2');
// require('lg-video');
// require('lightgallery');

import 'vimeo-froogaloop2';
import 'lightgallery';
import 'lg-video';

var jQueryBridget = require( 'jquery-bridget' );
var Masonry = require( 'masonry-layout' );
var InfiniteScroll = require( 'infinite-scroll' );
var ImagesLoaded = require( 'imagesloaded' );

InfiniteScroll.imagesLoaded = ImagesLoaded;

jQueryBridget( 'masonry', Masonry, $ );
jQueryBridget( 'infiniteScroll', InfiniteScroll, $ );
jQueryBridget( 'ImagesLoaded', ImagesLoaded, $ );

function owl_carousel() {
    var owl = $('.owl-carousel');

    owl.each(function () {
        $(this).owlCarousel({
            items: 1,
            onInitialized: callback
        });
        $(this).on('translated.owl.carousel', function (event) {
            $grid.masonry('reloadItems');
            $grid.masonry('layout');
        });
    });

    function callback(event) {
        var items_count = event.item.count;
        console.log(items_count);
        if (items_count <= 1) {
            this.settings.items = 1;
            this.settings.loop = false;
            this.settings.nav = false;
            this.settings.dots = false;
            this.settings.mouseDrag = false;
            this.settings.touchDrag = false;
            this.settings.pullDrag = false;
        } else {
            this.settings.items = 1;
            this.settings.loop = true;
            this.settings.nav = true;
            this.settings.dots = true;

            var h = 0;
            $(event.target).find(".owl-image-container").each(function () {
                if ($(this).outerHeight() > h) {
                    h = $(this).outerHeight();
                }
            });

            $(event.target).find(".owl-image-container").each(function () {
                $(this).css({
                    'height': h,
                    'display': 'flex',
                    'align-items': 'center',
                    'background-color': '#fff'
                });
            });
        }
    }
}

function lightGallery_init() {
    $('[id*=media-gallery]').lightGallery({
        controls: false,
        closable: true,
        download: false,
        fullscreen: true,
        googlePlus: false,
        thumbnail: false,
        selector: '.item'
    });
}

var $grid = $('.grid').masonry({
    itemSelector: 'none',
    columnWidth: 320,
    gutter: 0,
    fitWidth: true,
    transitionDuration: '0.8s',
    visibleStyle: { transform: 'translateY(0)', opacity: 1 },
    hiddenStyle: { transform: 'translateY(100px)', opacity: 0 }
});

var msnry = $grid.data('masonry');

$grid.ImagesLoaded(function () {
    owl_carousel();
    $grid.removeClass('grid-initial-state');
    $grid.masonry('option', { itemSelector: '.grid-item' });
    var $items = $grid.find('.grid-item');
    $grid.masonry('appended', $items );
 });

$grid.infiniteScroll({
    path: function() {
        if ( this.loadCount < pages_count ) {
            var page_number = this.loadCount + 2;
            if (typeof tag !== 'undefined') {
                return '/portfolio/filter/tag/' + tag + '/' + page_number + '/';
            } else if (typeof category !== 'undefined'){
                return '/portfolio/filter/category/' + category + '/' + page_number + '/';
            } else {
                return '/portfolio/filter/page/' + page_number + '/';
            }
        }
    },
    append: '.grid-item',
    outlayer: msnry,
    status: '.grid-load-status',
    history: false,
    loadOnScroll: true,
    onInit: function() {
        this.on( 'append', function(response, path, items) {
            var $new_items = $(items);
            $new_items.ImagesLoaded(function(){
                owl_carousel();
                $grid.masonry('option', { itemSelector: '.grid-item' });
                $grid.append($new_items).masonry( 'appended', $new_items );

                $(window).trigger('resize');
                lightGallery_init();
            });
        });
    }
});

$(window).resize(function () {
    $grid.masonry('reloadItems');
    $grid.masonry('layout');
});

$(document).ready(function() {
    lightGallery_init();
});