;; Eval Buffer with `M-x eval-buffer' to register the newly created template.

(dap-register-debug-template
  "Python :: Run editor"
  (list :type "python"
        :args ["platline.yaml"]
        :cwd nil
        :env '(("DEBUG" . "1"))
        :module nil
        :program "editor.py"
        :request "launch"
        :name "GTRG :: Run editor"))
