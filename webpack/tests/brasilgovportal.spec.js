describe('entry', function() {

    beforeEach(function() {
        let fileInjector = require('inject-loader!../app/brasilgovportal');
        this.filea = {
            getSpecialValue: function() {
                return 1;
            }
        };
        this.entry = fileInjector({
            './js/filea': this.filea
        });
        sinon.spy(this.filea, 'getSpecialValue');
    });

    it('works without override', function() {
        expect(require('../app/brasilgovportal.js').getValue()).to.equal(20);
    });

    it('overrides', function() {
        expect(this.entry.getValue()).to.equal(2);
    });

    it('gets a special value from filea', function() {
        this.entry.getValue();
        expect(this.filea.getSpecialValue.calledOnce).to.be.true;
    });

});
