import $ from 'jquery';
import jQuery from 'jquery';

import 'vimeo-froogaloop2';
import 'lightgallery';
import 'lg-video';

$(document).ready(function() {
    $("#media-gallery").lightGallery({
        controls: false,
        closable: true,
        download: false,
        fullscreen: true,
        googlePlus: false,
        thumbnail: false,
        selector: '.item'
    });
});

import 'lightgallery/src/sass/lightgallery.scss';
import '../scss/index.scss';