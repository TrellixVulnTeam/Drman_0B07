var SliderGx = (function() {

    if (!Array.prototype.forEach) {
        Array.prototype.forEach = function(callback/*, thisArg*/) {
            var T, k;
            if (this == null) {
                throw new TypeError('this is null or not defined');
            }
            var O = Object(this);
            var len = O.length >>> 0;
            if (typeof callback !== 'function') {
                throw new TypeError(callback + ' is not a function');
            }
            if (arguments.length > 1) {
                T = arguments[1];
            }
            k = 0;
            while (k < len) {
            var kValue;
            if (k in O) {
                kValue = O[k];
                callback.call(T, kValue, k, O);
            }
            k++;
            }
        };
    }

    function addClass(el, className) {
        if (el.classList) {
            el.classList.add(className);
        } else if (!hasClass(el, className)) {
            el.className += " " + className;
        }
    }

    function removeClass(el, className) {
        if (el.classList) {
            el.classList.remove(className);
        } else if (hasClass(el, className)) {
            var reg = new RegExp('(\\s|^)' + className + '(\\s|$)');
            el.className=el.className.replace(reg, ' ');
        }
    }

    function hasClass(element, cls) {
        return (' ' + element.className + ' ').indexOf(' ' + cls + ' ') > -1;
    }

    function SliderGx(args) {
        var root = this;
        this.slider = args.slider,
        this.btnPrev = args.btnPrev,
        this.btnNext = args.btnNext
    }

    function isInPage(node) {
        return (node === document.body) ? false : document.body.contains(node);
    }

    SliderGx.prototype.setSliderHeight = function(el) {
        this.slider.style.height = el.offsetHeight+'px';
    }

    SliderGx.prototype.moving = function(next) {
        var all = this.slider.querySelectorAll('.jsSliderBlock'),
            active,
            next,
            isMoving = true,
            arrIndex;
        all.forEach(function(element, index, array) {
            if(hasClass(element, 'active') === true) {
                active = element;
                if(next === true) {
                    arrIndex = index+1;
                    if(array.length > arrIndex) {
                        next = array[index+1];
                    } else {
                        isMoving = false;
                    }
                } else {
                    arrIndex = index-1;
                    if(arrIndex !== -1) {
                        next = array[index-1];
                    } else {
                        isMoving = false;
                    }
                }
            }
        }, this);
        if(isMoving === true) {
            removeClass(active, 'active');
            addClass(next, 'active');
            this.setSliderHeight(next);
        }
    }

    SliderGx.prototype.next = function() {
        this.moving(true);
    }

    SliderGx.prototype.prev = function() {
        this.moving(false);
    }

    SliderGx.prototype.play = function() {

    }

    SliderGx.prototype.stop = function() {

    }

    SliderGx.prototype.init = function() {
        if(isInPage(this.slider)) {

            var self = this;
            if (isInPage(this.btnPrev)) {
                this.btnPrev.addEventListener("click", this.prev.bind(this), false);
            }

            if (isInPage(this.btnNext)) {
                this.btnNext.addEventListener("click", this.next.bind(this), false);
            }

            if(this.slider) {
                var active = this.slider.querySelector('.jsSliderBlock.active');
                this.setSliderHeight(active);
                window.addEventListener('resize', function() {
                    var current = self.slider.querySelector('.jsSliderBlock.active');
                    self.setSliderHeight(current);
                });
                this.slider.querySelector('.jsSlider img:last-child').addEventListener('load', function(e) {
                    self.setSliderHeight(active);
                }, false);
            }

        } else {
            return false;
        }
    }

    return SliderGx;

}());