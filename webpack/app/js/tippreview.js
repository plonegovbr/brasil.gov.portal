import tippy from 'tippy.js';


export default class TipPreview {
  constructor() {
    this.$template = $('<div>');
    this.$template.html(
      `<div class="tippreview">
        <div class="tippreview-image">
          <img src="" alt="" />
        </div>
        <div class="tippreview-title">
          Page title
        </div>
      </div>`
    );

    // don't show preview on edit tab
    if ($('#contentview-edit.selected').length > 0) {
      return;
    }

    // Change this option when style the tooltip
    this.dontHide = false;

    this.createTooltip();
  }
  createTooltip() {
    tippy('[data-tippreview-enabled="true"]', {
      animation: 'shift-toward',
      arrow: true,
      theme: 'light',
      html: this.$template[0],
      onShow: this.onShow.bind(this),
      // prevent tooltip from displaying over button
      popperOptions: {
        modifiers: {
          preventOverflow: {
            enabled: false
          },
          hide: {
            enabled: false
          }
        }
      }
    });
  }
  onShow(tip) {
    if (this.dontHide) {
      tip.hide = function() {};
    }

    let $a = $(tip.reference);

    let $image = $('.tippreview-image > img', this.$template);
    $image.attr('src', $a.attr('data-tippreview-image'));

    let $title = $('.tippreview-title', this.$template);
    $title.html($a.attr('data-tippreview-title'));
  }
}
