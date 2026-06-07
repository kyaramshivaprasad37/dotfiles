;;; $DOOMDIR/config.el -*- lexical-binding: t; -*-

;; Place your private configuration here! Remember, you do not need to run 'doom
;; sync' after modifying this file!


;; Some functionality uses this to identify you, e.g. GPG configuration, email
;; clients, file templates and snippets. It is optional.
;; (setq user-full-name "John Doe"
;;       user-mail-address "john@doe.com")

;; Doom exposes five (optional) variables for controlling fonts in Doom:
(setq doom-font (font-spec :family "Monospace" :size 14))
;;
;; - `doom-font' -- the primary font to us
;; - `doom-variable-pitch-font' -- a non-monospace font (where applicable)
;; - `doom-big-font' -- used for `doom-big-font-mode'; use this for
;;   presentations or streaming.
;; - `doom-symbol-font' -- for symbols
;; - `doom-serif-font' -- for the `fixed-pitch-serif' face
;;
;; See 'C-h v doom-font' for documentation and more examples of what they
;; accept. For example:
;;
;;(setq doom-font (font-spec :family "JetBrains Mono" :size 14)
;;     doom-variable-pitch-font (font-spec :family "Ubuntu" :size 15))
;;
;; If you or Emacs can't find your font, use 'M-x describe-font' to look them
;; up, `M-x eval-region' to execute elisp code, and 'M-x doom/reload-font' to
;; refresh your font settings. If Emacs still can't find your font, it likely
;; wasn't installed correctly. Font issues are rarely Doom issues!

;; There are two ways to load a theme. Both assume the theme is installed and
;; available. You can either set `doom-theme' or manually load a theme with the
;; `load-theme' function. This is the default:
(setq doom-theme 'doom-tokyo-night)

;; This determines the style of line numbers in effect. If set to `nil', line
;; numbers are disabled. For relative line numbers, set this to `relative'.
(setq display-line-numbers-type t)

;; If you use `org' and don't want your org files in the default location below,
;; change `org-directory'. It must be set before org loads!
(setq org-directory "~/org/")


;; Whenever you reconfigure a package, make sure to wrap your config in an
;; `after!' block, otherwise Doom's defaults may override your settings. E.g.
;;
;;   (after! PACKAGE
;;     (setq x y))
;;
;; The exceptions to this rule:
;;
;;   - Setting file/directory variables (like `org-directory')
;;   - Setting variables which explicitly tell you to set them before their
;;     package is loaded (see 'C-h v VARIABLE' to look up their documentation).
;;   - Setting doom variables (which start with 'doom-' or '+').
;;
;; Here are some additional functions/macros that will help you configure Doom.
;;
;; - `load!' for loading external *.el files relative to this one
;; - `use-package!' for configuring packages
;; - `after!' for running code after a package has loaded
;; - `add-load-path!' for adding directories to the `load-path', relative to
;;   this file. Emacs searches the `load-path' when you load packages with
;;   `require' or `use-package'.
;; - `map!' for binding new keys
;;
;; To get information about any of these functions/macros, move the cursor over
;; the highlighted symbol at press 'K' (non-evil users must press 'C-c c k').
;; This will open documentation for it, including demos of how they are used.
;; Alternatively, use `C-h o' to look up a symbol (functions, variables, faces,
;; etc).
;;
;; You can also try 'gd' (or 'C-c c d') to jump to their definition and see how
;; they are implemented.
(setq org-agenda-files '("~/org/todo.org"))
(setq org-roam-directory (file-truename "~/org/roam"))
(setq org-babel-python-command "python3")
(setq org-babel-default-header-args:python'((:results . "output")))
(setq org-hide-emphasis-markers t)

(setq org-roam-capture-templates
      '(("d" "default" plain "%?"
         :target (file+head "${slug}.org"
                            "#+title: ${title}\n")
         :unnarrowed t)))
(use-package! org-roam-ui
  :after org-roam
  :config
  (setq org-roam-ui-sync-theme t
        org-roam-ui-follow t
        org-roam-ui-update-on-save t
        org-roam-ui-open-on-start t))

;; ~/.config/doom/config.el
(use-package! yasnippet
  :config
  (yas-global-mode 1))

;; Optional: make sure we load personal snippets
(setq yas-snippet-dirs
      (append yas-snippet-dirs
              '("~/.config/doom/snippets")))
(after! org-roam
  (setq org-roam-capture-templates
        '(("d" "dbms" plain "%?"
           :target (file+head "%<%Y%m%d%H%M%S>-${slug}.org"
                              "#+title: ${title}\n#+filetags: :dbms:\n#+PROPERTY: header-args:sql :engine mysql :dbuser root :dbpassword :database dbms_lab\n")
           :unnarrowed t)
          ("n" "default" plain "%?"
           :target (file+head "%<%Y%m%d%H%M%S>-${slug}.org"
                              "#+title: ${title}\n")
           :unnarrowed t))))
;; Tsoding-style C config
(after! cc-mode
  (setq-default c-basic-offset 4
                c-default-style '((java-mode . "java")
                                  (awk-mode . "awk")
                                  (other . "bsd")))
  (add-hook 'c-mode-hook (lambda ()
                           (c-toggle-comment-style -1))))

;; Trim trailing whitespace on save for C
(add-hook 'c-mode-hook (lambda ()
                         (add-to-list 'write-file-functions
                                      'delete-trailing-whitespace)))

;; Multiple cursors (Tsoding style)
(after! multiple-cursors
  (global-set-key (kbd "C->") 'mc/mark-next-like-this)
  (global-set-key (kbd "C-<") 'mc/mark-previous-like-this)
  (global-set-key (kbd "C-c C-<") 'mc/mark-all-like-this))

;; Magit shortcuts
(global-set-key (kbd "C-c m s") 'magit-status)
(global-set-key (kbd "C-c m l") 'magit-log)

;; Move lines up/down like Tsoding
(global-set-key (kbd "M-p") 'move-text-up)
(global-set-key (kbd "M-n") 'move-text-down)

(after! elfeed
  (evil-define-key 'normal elfeed-search-mode-map
    (kbd "j") 'next-line
    (kbd "k") 'previous-line
    (kbd "J") 'elfeed-goodies/next-entry-and-preview
    (kbd "K") 'elfeed-goodies/prev-entry-and-preview))
(after! org
  (map! :map org-mode-map
        :localleader
        "cc" (lambda ()
               (interactive)
               (let* ((info (org-babel-get-src-block-info))
                      (code (nth 1 info))
                      (tmpfile "/tmp/org_run.c"))
                 (write-region code nil tmpfile)
                 (vterm-other-window)
                 (vterm-send-string
                  (format "gcc %s -o /tmp/org_run && /tmp/org_run\n" tmpfile))))))

