        root.grid_columnconfigure(3, weight=1)
        root.grid_rowconfigure(0, weight=1)

        # -------- Bảng hiển thị chỉ số thuật toán --------
        metrics_frame = tk.Frame(self.right_panel)
        metrics_frame.pack(fill="both", expand=True)

        self.metrics_tree = ttk.Treeview(
            metrics_frame,
            columns=("metric", "value"),
            show="headings",
        )
        self.metrics_tree.heading("metric", text="Chỉ số")
        self.metrics_tree.heading("value", text="Giá trị")
        self.metrics_tree.column("metric", width=160, anchor="w")
        self.metrics_tree.column("value", width=180, anchor="center")

        metrics_scrollbar = ttk.Scrollbar(metrics_frame, orient="vertical", command=self.metrics_tree.yview)
        self.metrics_tree.configure(yscrollcommand=metrics_scrollbar.set)

        self.metrics_tree.pack(side="left", fill="both", expand=True)
        metrics_scrollbar.pack(side="right", fill="y")

        # -------- Seed log với scrollbar --------
        seed_frame = tk.Frame(self.right_panel)
        seed_frame.pack(fill="both", expand=True, pady=(10, 0))

        tk.Label(seed_frame, text="Lịch sử Seed").pack(anchor="w")

        self.seed_listbox = tk.Listbox(seed_frame)
        self.seed_listbox.pack(side="left", fill="both", expand=True)

        seed_scrollbar = tk.Scrollbar(seed_frame, orient="vertical", command=self.seed_listbox.yview)
        seed_scrollbar.pack(side="right", fill="y")

        self.seed_listbox.config(yscrollcommand=seed_scrollbar.set)

        # Label seed hiện tại
        self.current_seed_label = tk.Label(self.right_panel, text="Seed hiện tại: None")
        self.current_seed_label.pack(pady=(5, 10), anchor="w")

        # Double click chọn seed
        self.seed_listbox.bind("<Double-1>", self.on_seed_double_click)