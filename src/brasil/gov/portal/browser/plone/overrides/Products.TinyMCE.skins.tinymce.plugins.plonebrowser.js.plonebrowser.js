/*jslint regexp: true,
         browser: true,
         sloppy: true,
         white: true,
         plusplus: true,
         indent: 4,
         maxlen: 200 */
/*global jq, tinymce, tinyMCEPopup, alert */
/**
 * Image selection dialog.
 *
 * @param mcePopup Reference to a corresponding TinyMCE popup object.
 */
var BrowserDialog = function (mcePopup) {
    var image_list_url, link_list_url;
    var jq = top.jQuery;

    this.tinyMCEPopup = mcePopup;
    this.editor = mcePopup.editor;

    /* In case of UID linked images maintains a relative "resolveuid/<UUID>"
       fragment otherwise contains a full URL to the image. */
    this.current_link = "";

    /* Absolute base URL to an image (without scaling path components)
       regardless whether the image was referenced using an UID or a direct
       link. */
    this.current_url = "";

    /* List of additional CSS classes set on the <img/> element which have no
       special meaning for TinyMCE. These are passed through as is. */
    this.current_classes = [];
    this.is_search_activated = false;

    /* Translatable UI labels */
    this.labels = this.editor.getParam("labels");

    /* URL of the thumbnail image shown on the right side details pane when
       an image is selected.  */
    this.thumb_url = "";

    /* Hold state if we are updateing image */
    this.editing_existing_image = false;

    // TODO: WTF?
    image_list_url = this.tinyMCEPopup.getParam("external_image_list_url");
    if (image_list_url) {
        jq.getScript(this.editor.documentBaseURI.toAbsolute(image_list_url));
    }
    link_list_url = tinyMCEPopup.getParam("external_link_list_url");
    if (link_list_url) {
        jq.getScript(this.editor.documentBaseURI.toAbsolute(link_list_url));
    }
};


/**
 * Dialog initialization.
 *
 * This will be called when the dialog is activated by pressing the
 * corresponding toolbar icon.
 */
BrowserDialog.prototype.init = function () {
    var self = this,
        jq = top.jQuery,
        selected_node = jq(this.editor.selection.getNode(), document),
        scaled_image,
        mailaddress,
        mailsubject,
        href,
        current_uid;

    this.tinyMCEPopup.resizeToInnerSize();

    // Determine type of the plugin: link or image
    this.is_link_plugin = window.location.search.indexOf('plonelink') > -1;
    this.method_folderlisting = this.is_link_plugin ? 'tinymce-jsonlinkablefolderlisting' : 'tinymce-jsonimagefolderlisting';
    this.method_search = this.is_link_plugin ? 'tinymce-jsonlinkablesearch' : 'tinymce-jsonimagesearch';
    this.shortcuts_html = this.is_link_plugin ? self.editor.settings.link_shortcuts_html : self.editor.settings.image_shortcuts_html;

    // Setup events
    jq('#insert-selection', document).click(function (e) {
        e.preventDefault();
        if (self.is_link_plugin === true) {
            self.insertLink();
        } else {
            self.insertImage();
        }
    });
    jq('#cancel', document).click(function (e) {
        e.preventDefault();
        self.tinyMCEPopup.close();
    });
    jq('#upload', document).click(function (e) {
        e.preventDefault();
        self.displayPanel('upload');
    });
    jq('#uploadbutton', document).click(function (e) {
        e.preventDefault();
        jq('#upload_form', document).submit();
    });
    jq('#searchtext', document).keyup(function (e) {
        e.preventDefault();
        // We need to stop the event from propagating so that pressing Esc will
        // only stop the search but not close the whole dialog.
        e.stopPropagation();
        self.checkSearch(e);
    });
    jq('#clear-btn', document).click(function (e) {
        e.preventDefault();
        jq('#searchtext', document).val("");
        self.checkSearch(e);
    });
    jq('#search-btn', document).click(function (e) {
        e.preventDefault();
        self.checkSearch(e);
    });
    // handle shortcuts button
    jq("#shortcutsicon", document).click(function (e) {
        e.preventDefault();
        jq(this).toggleClass('selected');
        jq('#shortcutsview', document).toggle();
    });

    // handle different folder listing view types
    jq('#general_panel .legend a', document).click(function (e) {
        self.editing_existing_image = true;
        e.preventDefault();
        jq('#general_panel .legend a', document).removeClass('current');
        jq(this).addClass('current');
        // refresh listing with new view settings
        self.getFolderListing(self.folderlisting_context_url, self.folderlisting_method);
    });

    // setup UI based on settings
    if (!this.editor.settings.allow_captioned_images) {
        jq('#caption', document).parent().parent().hide();
    }
    if (this.editor.settings.rooted === true) {
        jq('#home', document).hide();
    }
    if (!this.editor.settings.enable_external_link_preview) {
        jq('#preview-column', document).hide();
    }

    // setup UI depending on plugin type
    if (this.is_link_plugin === true) {
        // we may have image selected and anchor is the wrapping node
        selected_node = selected_node.closest('a');
        jq('#browseimage_panel h2', document).text(this.labels.label_browselink);
        jq('#addimage_panel h2', document).text(this.labels.label_addnewfile);
        jq('#plonebrowser', document).removeClass('image-browser').addClass('link-browser');

        this.populateAnchorList();

        // display results as list and disable thumbs view
        jq('.legend a', document).removeClass('current');
        jq('#listview', document).addClass('current');
        jq('.legend', document).hide();

        // setup link buttons acions
        jq('#linktype a', document).click(function (e) {
            e.preventDefault();
            jq('#linktype_panel div', document).removeClass('current');
            jq(this, document).parent('div').addClass('current');
            switch (jq(this).attr('href')) {
                case "#internal":
                    self.displayPanel('browse');
                    self.getCurrentFolderListing();
                    break;
                case "#external":
                    self.displayPanel('external');
                    break;
                case "#email":
                    self.displayPanel('email');
                    break;
                case "#anchor":
                    self.displayPanel('anchor');
                    break;
            }
        });
        jq('#externalurl', document).keyup(function (e) {
            self.checkExternalURL(this.value);
        });
        jq('#targetlist', document).change(this.setupPopupVisibility);
        jq('#previewexternalurl', document).click(function (e) {
            e.preventDefault();
            jq('#previewexternal', document).show();
            jq(this).text('Refresh Preview');
            self.previewExternalURL();
        });

        /* handle link plugin startup */
        if (selected_node.length > 0 && selected_node[0].nodeName.toUpperCase() === "A") {
            // element is anchor, we have a link
            href = jq.trim(selected_node.attr('href'));

            // setup form data
            if ((typeof(selected_node.attr('title')) !== "undefined")) {
                jq('#title', document).val(selected_node.attr('title'));
            }

            // determine link type
            if (href.indexOf('#') === 0) {
                // anchor
                jq('input:radio[value=' + href + ']', document).click();
                jq('#linktype a[href=#anchor]', document).click();
                jq('#cssstyle', document).val(selected_node.attr('style'));
            } else if (href.indexOf('mailto:') > -1) {
                // email
                href = href.split('mailto:')[1].split('?subject=');
                if (href.length === 2) {
                    mailaddress = href[0];
                    mailsubject = href[1];
                } else {
                    mailaddress = href[0];
                    mailsubject = "";
                }

                jq('#mailaddress', document).val(mailaddress);
                jq('#mailsubject', document).val(mailsubject);
                jq('#cssstyle', document).val(selected_node.attr('style'));
                jq('#linktype a[href=#email]', document).click();
            } else if ((href.indexOf(this.editor.settings.portal_url) === -1) &&
                ((href.indexOf('http://') === 0) || (href.indexOf('https://') === 0) || (href.indexOf('ftp://') === 0))) {
                // external
                this.checkExternalURL(href);
                jq('#cssstyle', document).val(selected_node.attr('style'));
                jq('#linktype a[href=#external]', document).click();
            } else {
                // internal
                if (href.indexOf('#') !== -1) {
                    href = href.split('#')[0];
                }
                // mark we are selecting an item in browser
                this.editing_existing_image = true;

                if (href.indexOf('resolveuid') !== -1) {
                    current_uid = href.split('resolveuid/')[1];
                    jq.ajax({
                        url: this.editor.settings.portal_url + '/portal_tinymce/tinymce-getpathbyuid?uid=' + current_uid,
                        dataType: 'text',
                        type: 'GET',
                        success: function (text) {
                            self.current_url = self.getAbsoluteUrl(self.editor.settings.document_base_url, text);
                            self.current_link = self.editor.settings.link_using_uids ? href : self.current_url;
                            self.getFolderListing(self.getParentUrl(self.current_url), 'tinymce-jsonlinkablefolderlisting');
                        }
                    });
                } else {
                    this.current_link = this.getAbsoluteUrl(this.editor.settings.document_base_url, href);
                    this.getFolderListing(this.getParentUrl(this.current_link), 'tinymce-jsonlinkablefolderlisting');
                }
                jq('#cssstyle', document).val(selected_node.attr('style'));
            }

            jq('#targetlist', document).val(selected_node.attr('target'));
            // TODO: set the rest of the "advanced" fields that are in common for all of them
        } else {
            // plain text selection
            href = jq.trim(this.editor.selection.getContent());
            if ((href.indexOf('http://') === 0) || (href.indexOf('https://') === 0) || (href.indexOf('ftp://') === 0)) {
                this.checkExternalURL(href);
                jq('#linktype a[href=#external]', document).click();
            } else {
                this.getCurrentFolderListing();
            }
        }

    } else {
        /* handle image plugin startup */
        // jq('#browseimage_panel h2', document).text(this.labels.label_browseimage);
        jq('#addimage_panel h2', document).text(this.labels.label_addnewimage);
        jq('#plonebrowser', document).removeClass('link-browser').addClass('image-browser');
        jq('#linktarget', document).hide();

        // setup panel buttons acions
        jq('#email_link, #anchor_link', document).hide();
        jq('#linktype a', document).click(function (e) {
            e.preventDefault();
            jq('#linktype_panel div', document).removeClass('current');
            jq(this, document).parent('div').addClass('current');
            switch (jq(this).attr('href')) {
                case "#internal":
                    self.displayPanel('browse');
                    self.getCurrentFolderListing();
                    break;
                case "#external":
                    self.displayPanel('externalimage');
                    break;
            }
        });

        jq('#previewimagebutton', document).click(function (e) {
            var url = jq('#imageurl', document).val();
            e.preventDefault();
            jq('#imgpreview', document).html('<img src="' + url + '" />');
        });

        if (selected_node.get(0).tagName && selected_node.get(0).tagName.toUpperCase() === 'IMG') {
            /** The image dialog was opened to edit an existing image element. **/
            this.editing_existing_image = true;

            // Manage the CSS classes defined in the <img/> element. We handle the
            // following classes as special cases:
            //   - captioned
            //   - image-inline
            //   - image-left
            //   - image-right
            // and pass all other classes through as-is.
            jq.each(selected_node.attr('class').split(/\s+/), function () {
                var classname = this.toString();
                switch (classname) {
                    case 'captioned':
                        if (self.editor.settings.allow_captioned_images) {
                            // Check the caption checkbox
                            jq('#caption', document).attr('checked', 'checked');
                        }
                        break;

                    case 'image-inline':
                    case 'image-left':
                    case 'image-right':
                        // Select the corresponding option in the "Alignment" <select>.
                        jq('#classes', document).val(classname);
                        break;

                    default:
                        // Keep track of custom CSS classes so we can inject them
                        // back into the element later.
                        self.current_classes.push(classname);
                        break;
                }
            });

            if (selected_node.get(0).classList) {
                var is_external = selected_node.get(0).classList.contains('external-image');
            }
            else {
                // Needed for IE8 and IE9, which do not have 'classList'.
                var is_external = (' ' + selected_node.get(0).className + ' ').indexOf('external-image') > -1;
            }
            if (is_external) {
                self.displayPanel('externalimage');
                jq('#linktype_panel div', document).removeClass('current');
                jq('#external_link', document).addClass('current');
                jq('#imagetitle', document).val(selected_node.get(0).alt);
                jq('#imageurl', document).val(selected_node.get(0).src);
            } else {
                scaled_image = this.parseImageScale(selected_node.attr("src"));

                // Store the selected scale on the dimensions <select>.
                jq('#dimensions', document).data('selectedScale', scaled_image.scale);

                if (scaled_image.url.indexOf('resolveuid/') > -1) {
                    /** Handle UID linked image **/

                    current_uid = scaled_image.url.split('resolveuid/')[1];

                    // Fetch the information about the UID linked image.
                    jq.ajax({
                        'url': this.editor.settings.portal_url + '/portal_tinymce/tinymce-getpathbyuid?uid=' + current_uid,
                        'dataType': 'text',
                        'type': 'GET',
                        'success': function (text) {
                            // Store the absolute URL to the UID referenced image
                            self.current_url = self.getAbsoluteUrl(self.editor.settings.document_base_url, text);
                            // Store the image link as UID or full URL based on policy
                            self.current_link = self.editor.settings.link_using_uids ? scaled_image.url : self.current_url;

                            self.getFolderListing(self.getParentUrl(self.current_url), 'tinymce-jsonimagefolderlisting');
                        }
                    });
                } else {
                    /** Handle directly linked image **/
                    this.current_link = this.getAbsoluteUrl(this.editor.settings.document_base_url, scaled_image.url);
                    this.getFolderListing(this.getParentUrl(this.current_link), 'tinymce-jsonimagefolderlisting');
                }
            }
        } else {
            /** The image dialog was opened to add a new image. **/
            this.getCurrentFolderListing();
        }
    }
};

/**
 * Parses the image scale (dimensions) from the given URL.
 *
 * The scale URLs used by plone.app.imaging are of the form
 *
 *   http://server.com/some-image.png/@@images/<field>/<scale>
 *
 * where <field> denotes the particular field containing the image and <scale>
 * identifies the particular image scale.
 *
 * For backward compatibility the previous form of image scale URLs is also
 * supported, but only for the "image" field, e.g.
 *
 *   http://server.com/some-image/image_<scale>
 *
 * where <scale> again denotes the particular image scale.
 *
 * Returns an object with the base URL to the image and another relative URL
 * to the image scale, e.g.
 *
 * { 'url': 'http://server.com/some-image',
 *   'scale' : '@@images/image/thumb' }
 *
 * The 'scale' key will always contain the plone.app.imaging type of scale
 * regardless of the original form, effectively rewriting everything to use
 * the @@images view.
 *
 * @param url URL to a possible scaled image.
 */
BrowserDialog.prototype.parseImageScale = function (url) {
    var parts,
        last_part,
        scale_pos,
        parsed = {
            "url": url,
            "scale": ""
        };

    if (url.indexOf('/') > -1) {
        parts = url.split('/');
        last_part = parts[parts.length - 1];

        if (last_part.indexOf('image_') > -1) {
            // This is an old-style scale URL. We'll translate the scale to
            // the form used by plone.app.imaging.
            parsed.scale = "@@images/image/" + parts.pop().substring(6);
            parsed.url = parts.join("/");
        } else {
            scale_pos = url.search(/@@images\/[^\/]+\/.+/);
            if (scale_pos > -1) {
                // This is a new style URL
                parsed.url = url.substring(0, scale_pos - 1);
                parsed.scale = url.substring(scale_pos);
            }
        }
    }

    return parsed;
};

/**
 * Given DOM node and href value, setup all node attributes/properies
 */
BrowserDialog.prototype.setLinkAttributes = function (node, link) {
    var jq = top.jQuery;
    var panelname = jq('#linktype .current a', document).attr('href');

    jq(node)
        .attr('href', link)
        .attr('data-mce-href', link)
        .attr('title', jq('#title', document).val())
        .attr('target', jq('#targetlist', document).val())
        .attr('style', jq('#cssstyle', document).val())
        .removeClass('internal-link external-link anchor-link mail-link')
        .addClass(panelname.substr(1, panelname.length) + '-link');
};


/**
 * Handle inserting the selected link into the DOM of the editable area.
 *
 */
BrowserDialog.prototype.insertLink = function () {
    var jq = top.jQuery;
    var selected_node = jq(this.editor.selection.getNode(), document),
        active_panel = jq('#linktype .current a', document).attr('href'),
        self = this,
        mailsubject,
        elementArray,
        i,
        nodes,
        url_match,
        link,
        name;

    if (selected_node.get(0).tagName !== "A") {
        selected_node = selected_node.parent('a');
        if (selected_node.length === 0) {
            selected_node = null;
        } else {
            selected_node = selected_node.get(0);
        }
    } else {
        selected_node = selected_node.get(0);
    }

    switch (active_panel) {
        case "#internal":
            link = this.editor.convertURL(this.current_link);

            anchor = jq('#pageanchor', document).val();
            if (anchor) {
                link += '#' + anchor;
            }
            break;
        case "#external":
            link = this.previewExternalURL();
            break;
        case "#email":
            link = jq('#mailaddress', document).val();
            mailsubject = jq('#mailsubject', document).val();
            if (mailsubject !== "") {
                link += "?subject=" + mailsubject;
            }
            if (link !== "") {
                link = "mailto:" + link;
            }
            break;
        case "#anchor":
            link = jq('#anchorlinkcontainer input:checked', document).val();
            url_match = link.match(/^#mce-new-anchor-(.*)$/);
            if (url_match !== null) {
                // create anchor link
                nodes = this.editor.dom.select(this.editor.settings.anchor_selector);
                for (i = 0; i < nodes.length; i++) {
                    name = jq(nodes[i]).text().replace(/^\s+|\s+$/g, '');
                    name = name.toLowerCase().substring(0, 1024).replace(/[^a-z0-9]/g, '-');

                    if (name === url_match[1]) {
                        nodes[i].innerHTML = '<a name="' + name + '" class="mceItemAnchor"></a>' + nodes[i].innerHTML;
                    }
                }
                link = '#' + url_match[1];
            }
            break;
    }

    // Remove element if there is no link
    if (!link) {
        this.tinyMCEPopup.execCommand("mceBeginUndoLevel");
        i = this.editor.selection.getBookmark();
        this.editor.dom.remove(selected_node, 1);
        this.editor.selection.moveToBookmark(i);
        this.tinyMCEPopup.execCommand("mceEndUndoLevel");
        this.tinyMCEPopup.close();
        return;
    }

    this.tinyMCEPopup.execCommand("mceBeginUndoLevel");

    if (selected_node === null) {
        // Create new anchor elements
        // no idea what this does, yet.
        this.editor.getDoc().execCommand("unlink", false, null);

        if (tinymce.isWebKit) {
            // https://github.com/tinymce/tinymce/pull/57#issuecomment-1771936
            img = this.editor.dom.getParent(this.editor.selection.getNode(), 'img');
            if (img !== null) {
                this.editor.getDoc().execCommand("insertHTML", false, "<a href='#mce_temp_url#'>"+img.outerHTML+"</a>");
            } else {
                this.tinyMCEPopup.execCommand("CreateLink", false, "#mce_temp_url#", {skip_undo : 1});
            }
        } else {
            this.tinyMCEPopup.execCommand("CreateLink", false, "#mce_temp_url#", {skip_undo : 1});
        }

        elementArray = tinymce.grep(this.editor.dom.select("a"), function(n) {
            return self.editor.dom.getAttrib(n, 'href') === '#mce_temp_url#';
        });
        for (i = 0; i < elementArray.length; i++) {
            this.setLinkAttributes(selected_node = elementArray[i], link);
        }
    } else {
        // Update attributes
        this.setLinkAttributes(selected_node, link);
    }

    // Don't move caret if selection was image
    if (selected_node && (selected_node.childNodes.length !== 1 || selected_node.firstChild.nodeName !== 'IMG')) {
        this.editor.focus();
        this.editor.selection.select(selected_node);
        this.editor.selection.collapse(0);
        this.tinyMCEPopup.storeSelection();
    }

    this.tinyMCEPopup.execCommand("mceEndUndoLevel");
    this.tinyMCEPopup.close();
};

/**
 * Handle inserting the selected image into the DOM of the editable area.
 *
 */
BrowserDialog.prototype.insertImage = function () {
    var attrs = {},
        jq = top.jQuery,
        selected_node = this.editor.selection.getNode(),
        href = this.editor.convertURL(this.current_link),
        active_panel = jq('#linktype .current a', document).attr('href'),
        dimension,
        classes;

    // Pass-through classes
    classes = [].concat(this.current_classes);
    // Alignment class
    classes.push(jq.trim(jq('#classes', document).val()));

    if (active_panel === "#external") {
        href = jq('#imageurl', document).val();
        if (jq.inArray('external-image', classes) === -1) {
            classes.push('external-image');
        }
        jq.extend(attrs, {
            alt: jq('#imagetitle', document).val(),
            title: jq('#imagetitle', document).val()
        });
    } else {
        // we have internal image panel

        // remove external-image if present
        if (jq.inArray('external-image', classes) > -1) {
            classes.splice(jq.inArray('external-image', classes), 1);
        }

        // Image captioning
        if (this.editor.settings.allow_captioned_images && jq('#caption', document).is(':checked')) {
            classes.push('captioned');
        }

        // if we have absolute url, make sure it's relative
        if (href.indexOf('resolveuid/') > -1) {
            href = 'resolveuid/' + href.split('resolveuid/')[1];
        }

        this.tinyMCEPopup.restoreSelection();

        // Fixes crash in Safari
        if (tinymce.isWebKit) {
            this.editor.getWin().focus();
        }

        // Append the image scale to the URL if a valid selection exists.
        dimension = jq('#dimensions', document).val();
        if (dimension !== "") {
            href += '/' + dimension;
        }
    }

    jq.extend(attrs, {
        'src' : href,
        'class' : classes.join(' ')
    });

    if (selected_node && selected_node.nodeName.toUpperCase() === 'IMG') {
        // Update an existing <img/> element
        this.editor.dom.setAttribs(selected_node, attrs);
    } else {
        // Create a new <img/> element.
        this.editor.execCommand('mceInsertContent', false, '<img id="__mce_tmp" />', {skip_undo : 1});
        this.editor.dom.setAttribs('__mce_tmp', attrs);
        this.editor.dom.setAttrib('__mce_tmp', 'id', '');
        this.editor.undoManager.add();
    }

    // Update the Description of the image
    if (active_panel === "#internal") {
        jq.ajax({
            'url': jq('#description_href', document).val() + '/tinymce-setDescription',
            'type': 'POST',
            'data': {
                'description': jq('#description', document).val()
            }
        });
    }

    this.tinyMCEPopup.close();
};

/**
 * Activates and disables the search feature based on user input.
 */
BrowserDialog.prototype.checkSearch = function (e) {
    var jq = top.jQuery;
    var el = jq('#searchtext', document),
        len = el.val().length;

    // Show the clear button when there is text in the search field
    if (len > 0) {
        jq('#clear-btn', document).show();
    }

    // Activate search when we have enough input and either livesearch is
    // enabled or the user explicitly pressed Enter (which === 13), or the user
    // clicks (which === 1) on the search icon
    if (len >= 3 && (this.tinyMCEPopup.editor.settings.livesearch === true
                    || e.which === 13 || e.which === 1)) {
        this.is_search_activated = true;
        this.getFolderListing(this.tinyMCEPopup.editor.settings.navigation_root_url, this.method_search);
    }

    // Disable search when we have no input or the user explicitly pressed the
    // Escape key.
    if ((len === 0 && this.is_search_activated) || e.which === 27) {
        this.is_search_activated = false;
        el.val('');
        this.getCurrentFolderListing();
    }

    if (len === 0 || e.which === 27) {
        jq('#clear-btn', document).hide();
    }
};

/**
 * Updates the details pane on the right by fetching image information from
 * the backend.
 *
 * After successful retrieval the right side pane will be updated with a
 * thumbnail of the selected image with information about the caption,
 * alignment and scale.
 *
 * @param url URL of the object to fetch.
 */
BrowserDialog.prototype.setDetails = function (url) {
    var jq = top.jQuery;
    var self = this,
        /**
         * Pretty-prints a human readable title for a image scale.
         */
        scale_title = function (scale) {
            if (scale.size[0]) {
                return scale.title + ' (' + scale.size[0] + 'x' + scale.size[1] + ')';
            } else {
                return scale.title;
            }
        };
    if (jq.trim(url).length === 0) {
        return;
    }

    jq.ajax({
        'url': url + '/tinymce-jsondetails',
        'dataType': 'json',
        'success': function (data) {
            var dimension = jq('#dimensions', document).data('selectedScale'),
                dimensions,
                i;

            // Add the thumbnail image to the details pane.
            if (data.thumb !== "") {
                jq('#previewimagecontainer', document)
                    .empty()
                    .append(jq('<img/>', document).attr({'src': data.thumb}));
                // Save the thumbnail URL for later use.
                self.thumb_url = data.thumb;
            } else {
                jq('#previewimagecontainer', document).empty();
                self.thumb_url = "";
            }

            jq('#description', document).val(data.description);
            jq('#description_href', document).val(data.url);

            // Repopulate the <option>s in the dimensions <select> element.
            if (data.scales) {
                dimensions = jq('#dimensions', document).empty();

                jq.each(data.scales, function () {
                    var scale = this,
                        option = jq('<option/>', document)
                            .attr({'value': scale.value})
                            .text(scale_title(scale));

                    if (option.val() === dimension) {
                        option.attr({'selected': 'selected'});
                    }
                    option.appendTo(dimensions);
                });
            }
            self.displayPanel('details');

            // select radio button in folder listing and mark selected image
            jq('input:radio[name=internallink][value!="' + data.uid_relative_url + '"]', document)
                .parent('.item')
                .removeClass('current');
            jq('input:radio[name=internallink][value="' + data.uid_relative_url + '"]', document)
                .attr('checked', 'checked')
                .parent('.item')
                .addClass('current');

            self.current_url = data.url;
            self.current_link = self.editor.settings.link_using_uids ? data.uid_relative_url : data.url;

            jq('#titledetails', document).text(data.title);
            if (self.is_link_plugin === true) {
                jq('#classes', document).parents('.field').addClass('hide');
                jq('#dimensions', document).parents('.field').addClass('hide');
            }

            if (data.anchors.length > 0) {
                html = '<option value="">top of page (default)</option>';
                for (i = 0; i < data.anchors.length; i++) {
                    html += '<option value="' + data.anchors[i] + '">' + data.anchors[i] + '</option>';
                }
                jq('#pageanchor', document).html(html);
                jq('#pageanchorcontainer', document).parents('.field').removeClass('hide');
            } else {
                jq('#pageanchorcontainer', document).parents('.field').addClass('hide');
            }
        }
    });
};

/**
 * Utility method to update the middle pane with the current context listing.
 */
BrowserDialog.prototype.getCurrentFolderListing = function () {
    this.getFolderListing(this.editor.settings.document_base_url, this.method_folderlisting);
};


/**
 * Updates the center pane with a listing of content from the given context.
 *
 * @param context_url URL of the context where the request will be made
 * @param method Name of the backed view to query
 */
BrowserDialog.prototype.getFolderListing = function (context_url, method) {
    var self = this;
    var jq = top.jQuery;

    // store this for view type refreshing
    this.folderlisting_context_url = context_url;
    this.folderlisting_method = method;

    jq.ajax({
        'url': context_url + '/' + method,
        'type': 'POST',
        'dataType': 'json',
        'data': {
            'searchtext': jq('#searchtext', document).val(),
            'rooted': this.editor.settings.rooted ? 'True' : 'False',
            'document_base_url': this.editor.settings.document_base_url
        },
        'success': function (data) {
            var html = [],
                len,
                current_uid,
                item_number = 0,
                folder_html = [],
                item_html = [],
                thumb_name = self.editor.settings.thumbnail_size[0],
                thumb_width = self.editor.settings.thumbnail_size[1],
                thumb_height = self.editor.settings.thumbnail_size[2],
                col_items_number = self.editor.settings.num_of_thumb_columns;

            if (data.items.length === 0) {
                html.push('<div id="no-items">' + self.labels.label_no_items + '</div>');
            } else {
                jq.each(data.items, function (i, item) {
                    if (item.url === self.current_link && self.editor.settings.link_using_uids) {
                        self.current_link = 'resolveuid/' + item.uid;
                    }
                    switch (jq('#general_panel .legend .current', document).attr('id')) {
                        // TODO: use jquery dom to be sure stuff is closed
                        case 'listview':
                            if (item.is_folderish) {
                                folder_html.push('<div class="list item folderish ' + (i % 2 === 0 ? 'even' : 'odd') + '">');
                                if (self.is_link_plugin === true) {
                                    jq.merge(folder_html, [
                                        '<input href="' + item.url + '" ',
                                            'type="radio" class="noborder" style="margin: 0; width: 16px" name="internallink" value="',
                                            'resolveuid/' + item.uid ,
                                            '"/> '
                                    ]);
                                } else {
                                    folder_html.push('<img src="img/arrow_right.png" />');
                                }
                                jq.merge(folder_html, [
                                        item.icon,
                                        '<a href="' + item.url + '" class="folderlink contenttype-' + item.normalized_type + ' state-' + item.review_state + '" title="' + item.description + ((item.description) ? '&#13;&#13;' : '') + item.path + '">',
                                            item.title,
                                        '</a>',
                                    '</div>'
                                ]);
                            } else {
                                jq.merge(item_html, [
                                    '<div class="item list ' + (i % 2 === 0 ? 'even' : 'odd') + '" title="' + item.description + ((item.description) ? '&#13;&#13;' : '') + item.path + '">',
                                        '<input href="' + item.url + '" ',
                                            'type="radio" class="noborder" style="margin: 0; width: 16px" name="internallink" value="',
                                            'resolveuid/' + item.uid ,
                                            '"/> ',
                                        '<span class="contenttype-' + item.normalized_type + ' state-' + item.review_state + '">' + item.title + '</span>',
                                    '</div>'
                                ]);
                            }
                            break;
                        case 'thumbview':
                            if (item_number % col_items_number === 0) {
                                item_html.push('<div class="row">');
                            }

                            if (item.is_folderish) {
                                jq.merge(item_html, [
                                    '<div class="width-1:' + col_items_number + ' cell position-' + item_number % col_items_number * (16 / col_items_number) + '">',
                                        '<div class="thumbnail item folderish" title="' + item.description +  '">',
                                            '<div style="width: ' + thumb_width + 'px; height: ' + thumb_height + 'px" class="thumb">',
                                                '<img src="img/folder_big.png" alt="' + item.title + '" />',
                                            '</div>',
                                            '<a href="' + item.url + '">',
                                                item.title,
                                            '</a>',
                                        '</div>',
                                    '</div>'
                                ]);
                            } else {
                                jq.merge(item_html, [
                                    '<div class="width-1:' + col_items_number + ' cell position-' + item_number % col_items_number * (16 / col_items_number) + '">',
                                        '<div class="thumbnail item" title="' + item.description +  '">',
                                            '<div style="width: ' + thumb_width + 'px; height: ' + thumb_height + 'px" class="thumb">',
                                                '<img src="' + item.url + '/@@images/image/' + thumb_name + '" alt="' + item.title + '" />',
                                            '</div>',
                                            '<p>' + item.title + '</p>',
                                            '<input href="' + item.url + '" ',
                                                'type="radio" class="noborder" name="internallink" value="',
                                                'resolveuid/' + item.uid,
                                                '"/> ',
                                        '</div>',
                                    '</div>'
                                ]);
                            }

                            if (item_number % col_items_number === col_items_number - 1) {
                                item_html.push('</div>');
                            }
                            item_number++;
                            break;
                    }


                });
            }
            jq.merge(html, folder_html);
            jq.merge(html, item_html);
            jq('#internallinkcontainer', document).html(html.join(''));

            // display shortcuts
            if (self.is_search_activated === false && self.shortcuts_html.length) {

                jqShortcutsBtn = jq('#shortcutsicon', document);
                jqShortcutsView = jq('#shortcutsview', document);
                jqShortcutItem = jq('#shortcutsview #item-template', document);

                jqShortcutsBtn.attr('title', self.labels.label_shortcuts);

                jq.each(self.shortcuts_html, function () {
                    jqItem = jqShortcutItem.clone();
                    jqItem.append(''+this);
                    jqItem.removeAttr('id');
                    jqItem.appendTo(jqShortcutsView);
                });
                jqShortcutItem.remove();

            }

            // Each time this function is called, a new event handler is created,
            // so we need to unbind all of them before continueing.
            // Namespace the events so we can unbind them easily

            // make rows clickable
            jq('#internallinkcontainer div.item', document)
                .unbind('.imagebrowser')
                .bind('click.imagebrowser', function() {
                    var el = jq(this),
                        checkbox = el.find('input');
                    if (checkbox.length > 0) {
                        checkbox.click();
                    } else {
                        el.find('a').click();
                    }
                });

            // breadcrumbs
            html = [];
            len = data.path.length;
            jq.each(data.path, function (i, item) {
                if (i > 0) {
                    html.push(" &rarr; ");
                }
                html.push(item.icon);
                if (i === len - 1) {
                    html.push('<span>' + item.title + '</span>');
                } else {
                    if (item.unaccessible) {
                      html.push('<em>' + item.title + '</em>');
                    } else {
                      html.push('<a href="' + item.url + '">' + item.title + '</a>');
                    }
                }
            });
            jq('#internalpath', document).html(html.join(''));

            // folder link action
            jq('#internallinkcontainer a, #internalpath a, #shortcutsview a', document)
                .unbind('.imagebrowser')
                .bind('click.imagebrowser', function(e) {
                    e.preventDefault();
                    e.stopPropagation();
                    self.getFolderListing(jq(this).attr('href'), self.method_folderlisting);
                });
            // item link action
            jq('#internallinkcontainer input:radio', document)
                .unbind('.imagebrowser')
                .bind('click.imagebrowser', function (e) {
                    e.preventDefault();
                    e.stopPropagation();
                    self.setDetails(jq(this).attr('href'));
                });

            // Make the image upload form upload the image into the current container.
            jq('#upload_form', document).attr('action', context_url + '/tinymce-upload');

            // Select image if we are updating existing one
            if (self.editing_existing_image === true) {
                self.editing_existing_image = false;
                if (self.current_link.indexOf('resolveuid/') > -1) {
                    current_uid = self.current_link.split('resolveuid/')[1];
                    jq.ajax({
                        'url': self.editor.settings.portal_url + '/portal_tinymce/tinymce-getpathbyuid?uid=' + current_uid,
                        'dataType': 'text',
                        'success': function(text) {
                            self.setDetails(self.getAbsoluteUrl(self.editor.settings.document_base_url, text));
                        }
                        // TODO: handle 410 (image was deleted)
                    });
                } else {
                    self.setDetails(self.current_link);
                }
            }
            self.displayPanel('browse', data.upload_allowed);

            // Handle search
            if (self.is_search_activated === true) {
                jq('#internalpath', document).prev().text(self.labels.label_search_results);
            } else {
                jq('#internalpath', document).prev().text(self.labels.label_internal_path);
            }
        }
    });
};

/**
 * Returns a URL to the parent (container) of the given URL.
 *
 * @param url URL with at least a single path component.
 */
BrowserDialog.prototype.getParentUrl = function (url) {
    var url_array = url.split('/');
    url_array.pop();
    return url_array.join('/');
};

/**
 * Returns an absolute URL based on a base url and a possibly relative link.
 *
 * If the given link is already an absolute URL it will be returned
 * unmodified, otherwise it will be joined with the base URL with any parent
 * references (..) factored out.
 *
 * @param base The base URL
 * @param link The link to calculate an absolute URL for
 */
BrowserDialog.prototype.getAbsoluteUrl = function (base, link) {
    var base_array,
        link_array,
        jq = top.jQuery,
        item;


    if ((link.indexOf('http://') > -1) || (link.indexOf('https://') > -1) || (link.indexOf('ftp://') > -1)) {
        return link;
    }

    base_array = base.split('/');
    link_array = link.split('/');

    // Remove document from base url
    base_array.pop();

    while (link_array.length > 0) {
        item = link_array.shift();
        if (item === ".") {
            // Do nothing
            jq.noop();
        } else if (item === "..") {
            // Remove leave node from base
            base_array.pop();
        } else {
            // Push node to base_array
            base_array.push(item);
        }
    }

    return base_array.join('/');
};
/*
 * Switch different panels and buttons
 *
 * @param panel Name of the panel to show
 * @param upload_allowed Boolean indication upload rights in current context
 */
BrowserDialog.prototype.displayPanel = function(panel, upload_allowed) {
    // handles: details, browse, search, external, email, anchor, upload, advanced
    var correction_length;
    var jq = top.jQuery;

    // handle upload button
    if ((upload_allowed === true || upload_allowed === undefined) && ((panel === "browse" || panel === "details") && this.is_search_activated === false)) {
        jq('#upload', document).attr('disabled', false).fadeTo(1, 1);
    } else {
        jq('#upload', document).attr('disabled', true).fadeTo(1, 0.5);
    }

    // handle email panel
    if (panel === "email") {
        jq('#email_panel', document).removeClass('hide');
        // move the common link fileds to appropriate location
        jq('#email_panel', document).append(jq('#common-link-fields', document).removeClass('hide'));
        jq('#insert-selection', document).removeAttr('disabled');
    } else {
        jq('#email_panel', document).addClass('hide');
    }
    // handle anchor panel
    if (panel === "anchor") {
        jq('#anchor_panel', document).removeClass('hide');
        // move the common link fileds to appropriate location
        jq('#anchorlinkcontainer', document).append(jq('#common-link-fields', document).removeClass('hide'));
        jq('#insert-selection', document).removeAttr('disabled');
    } else {
        jq('#anchor_panel', document).addClass('hide');
    }
    // handle external panel
    if (panel === "external") {
        jq('#external_panel', document).removeClass('hide');
        // move the common link fileds to appropriate location
        jq('#external-column', document).append(jq('#common-link-fields', document).removeClass('hide'));
        jq('#insert-selection', document).removeAttr('disabled');
    } else {
        jq('#external_panel', document).addClass('hide');
    }
    // show details panel, if an entry is selected
    checkedlink = jq("input:radio[name=internallink]:checked", document);
    if ((checkedlink.length === 1) && (panel === "browse")) {
      this.setDetails(jq(checkedlink).attr('value'));
    }

    // handle browse panel
    if (jq.inArray(panel, ["search", "details", "browse", "upload"]) > -1) {
        if (jq.inArray(panel, ["upload", "details"]) > -1) {
            jq('#browseimage_panel #general_panel', document).removeClass('width-full').addClass('width-3:4');
        } else {
            jq('#browseimage_panel #general_panel', document).removeClass('width-3:4').addClass('width-full');;
        }
        jq('#browseimage_panel', document).removeClass('hide').addClass('row');
        jq('#insert-selection', document).attr('disabled','disabled');
        jq('#upload-button', document).removeClass('hide');
    } else {
        jq('#browseimage_panel', document).removeClass('row').addClass('hide');
        jq('#upload-button', document).addClass('hide');
    }

    // handle details/preview panel
    if (panel === 'details') {
        jq('#details_panel', document).removeClass('hide');
        // move the common link fileds to appropriate location but only for the
        // internal link panel
        if( jq('#internal_link:visible', document).length > 0) {
            jq('#details-fields', document).append(jq('#common-link-fields', document).removeClass('hide'));
        }
        jq('#insert-selection', document).removeAttr('disabled');
    } else {
        jq('#details_panel', document).addClass('hide');
    }
    // handle upload panel
    if (panel === "upload") {
        jq('#addimage_panel', document).removeClass('hide');
    } else {
        jq('#addimage_panel', document).addClass('hide');
    }

    // handle external image
    if (panel === "externalimage") {
        jq('#externalimage_panel', document).removeClass('hide');
        jq('#insert-selection', document).removeAttr('disabled');
        jq('#imagetitle', document).parents('.field').after(jq('#classes', document).parents('.field'));
    } else {
        jq('#externalimage_panel', document).addClass('hide');
        jq('#caption', document).parents('.field').after(jq('#classes', document).parents('.field'));
    }
};

// Link type methods

/**
 * Retrieves anchors from current document and populates the list
 */
BrowserDialog.prototype.populateAnchorList = function () {
    var nodes,
        jq = top.jQuery,
        html = "",
        divclass = "even",
        name,
        title,
        title_match,
        nodes_length,
        i;

    nodes = this.editor.dom.select('a.mceItemAnchor,img.mceItemAnchor');
    nodes_length = nodes.length;
    for (i = 0; i < nodes_length; i++) {
        if ((name = this.editor.dom.getAttrib(nodes[i], "name")) !== "") {
            html += '<div class="' + divclass + '"><input type="radio" class="noborder" name="anchorlink" id="#' + name + '" value="#' + name + '"/> <label for="#' + name + '">' + name + '</label></div>';
            divclass = divclass === "even" ? "odd" : "even";
        }
        if ((name = nodes[i].id) !== "" && !nodes[i].href) {
            html += '<div class="' + divclass + '"><input type="radio" class="noborder" name="anchorlink" id="#' + name + '" value="#' + name + '"/> <label for="#' + name + '">' + name + '</label></div>';
            divclass = divclass === "even" ? "odd" : "even";
        }
    }

    nodes = this.editor.dom.select(this.editor.settings.anchor_selector);
    nodes_length = nodes.length;
    if (nodes.length > 0) {
        for (i = 0; i < nodes_length; i++) {
            title = jq(nodes[i]).text().replace(/^\s+|\s+$/g, '');
            if (title==='') {
              continue;
            }
            title_match = title.match(/mceItemAnchor/);
            if (title_match === null) {
                name = title.toLowerCase().substring(0,1024);
                name = name.replace(/[^a-z0-9]/g, '-');
                html += '<div class="' + divclass + '"><input type="radio" class="noborder" name="anchorlink" id="#mce-new-anchor-' + name + '" value="#mce-new-anchor-' + name + '"/><label for="#mce-new-anchor-' + name + '"> ' + title + '</label></div>';
                divclass = divclass === "even" ? "odd" : "even";
            }
        }
    }

    if (html === "") {
        html = '<div class="odd">'+ this.labels.label_no_anchors +'</div>';
    }

    jq('#anchorlinkcontainer', document).html(html);
};

/**
 * Strip HTTP scheme from URL and set prefix accordingly
 */
BrowserDialog.prototype.checkExternalURL = function (href) {
    var jq = top.jQuery;
    var el = jq('#externalurl', document),
        scheme = href.split('://')[0];

    if (href === undefined) {
        href = jq.trim(el.val());
    }

    if (jq.inArray(scheme, ['http', 'ftp', 'https']) > -1) {
        jq(el).val(href.substr(scheme.length + 3, href.length));
        jq('#externalurlprefix', document).val(scheme + '://');
    }
};

/**
 * Preview webpage if url is set
 */
BrowserDialog.prototype.previewExternalURL = function () {
    var jq = top.jQuery;
    var url = jq('#externalurl', document).val(),
        urlprefix = jq('#externalurlprefix', document).val();

    if (url === "") {
        jq('#previewexternal', document).attr('src', "about:blank");
        return "";
    } else {
        jq('#previewexternal', document).attr('src', urlprefix + url);
        return urlprefix + url;
    }
};

var bwrdialog = new BrowserDialog(tinyMCEPopup);
tinyMCEPopup.onInit.add(bwrdialog.init, bwrdialog);

/* These two functions are called from adapters.Upload.py
 * after uploadbutton was pressed
 */
var uploadOk = function uploadOk(current_link, folder) {
    var jq = top.jQuery;
    var filefield = jq('#uploadfile', document).parent();

    // redraw input selection for better UX feeling after successful upload
    filefield.html(filefield.html());

    bwrdialog.editing_existing_image = true;
    bwrdialog.current_link = current_link;
    bwrdialog.getFolderListing(folder, bwrdialog.method_folderlisting);
    bwrdialog.displayPanel('details');
};

var uploadError = function uploadError(current_link) {
    alert(current_link);
    // TODO: display ajax panel instead of alert
};
