package com.example.ch_admin;

import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.EditText;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.annotation.Nullable;
import androidx.fragment.app.Fragment;
import androidx.recyclerview.widget.LinearLayoutManager;
import androidx.recyclerview.widget.RecyclerView;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

public class MembersFragment extends Fragment {

    private static final int FILTER_ALL = 0, FILTER_ACTIVE = 1, FILTER_INACTIVE = 2;

    private final List<Member> allMembers = new ArrayList<>();
    private final MemberAdapter adapter = new MemberAdapter();

    private int currentFilter = FILTER_ALL;
    private String query = "";

    private TextView chipAll, chipActive, chipInactive, totalMembers, activeMembers;

    @Nullable
    @Override
    public View onCreateView(@NonNull LayoutInflater inflater, @Nullable ViewGroup container,
                             @Nullable Bundle savedInstanceState) {
        return inflater.inflate(R.layout.fragment_members, container, false);
    }

    @Override
    public void onViewCreated(@NonNull View view, @Nullable Bundle savedInstanceState) {
        super.onViewCreated(view, savedInstanceState);

        RecyclerView rv = view.findViewById(R.id.rvMembers);
        rv.setLayoutManager(new LinearLayoutManager(requireContext()));
        rv.setAdapter(adapter);

        chipAll = view.findViewById(R.id.chipAll);
        chipActive = view.findViewById(R.id.chipActive);
        chipInactive = view.findViewById(R.id.chipInactive);
        totalMembers = view.findViewById(R.id.total_members);
        activeMembers = view.findViewById(R.id.active_members);

        chipAll.setOnClickListener(v -> selectFilter(FILTER_ALL));
        chipActive.setOnClickListener(v -> selectFilter(FILTER_ACTIVE));
        chipInactive.setOnClickListener(v -> selectFilter(FILTER_INACTIVE));

        // "View All" resets the filter and the search box
        TextView tvViewAll = view.findViewById(R.id.tvViewAll);
        EditText etSearch = view.findViewById(R.id.etSearchMembers);
        tvViewAll.setOnClickListener(v -> {
            etSearch.setText("");
            selectFilter(FILTER_ALL);
        });

        etSearch.addTextChangedListener(new TextWatcher() {
            @Override public void beforeTextChanged(CharSequence s, int a, int b, int c) {}
            @Override public void onTextChanged(CharSequence s, int a, int b, int c) {}
            @Override public void afterTextChanged(Editable s) {
                query = s.toString().trim().toLowerCase(Locale.ROOT);
                applyFilter();
            }
        });

        // Sample data - replace with your real data (database / API)
        allMembers.add(new Member("John Doe", "MEM-001", true));
        allMembers.add(new Member("Jane Njeri", "MEM-002", true));
        allMembers.add(new Member("Peter Otieno", "MEM-003", true));
        allMembers.add(new Member("Grace Achieng", "MEM-004", false));
        allMembers.add(new Member("David Mugo", "MEM-005", true));

        chipAll.setSelected(true);   // "All" is selected when the screen opens
        updateSummary();
        applyFilter();
    }

    private void selectFilter(int filter) {
        currentFilter = filter;
        chipAll.setSelected(filter == FILTER_ALL);
        chipActive.setSelected(filter == FILTER_ACTIVE);
        chipInactive.setSelected(filter == FILTER_INACTIVE);
        applyFilter();
    }

    private void applyFilter() {
        List<Member> result = new ArrayList<>();
        for (Member m : allMembers) {
            boolean statusOk = currentFilter == FILTER_ALL
                    || (currentFilter == FILTER_ACTIVE && m.isActive())
                    || (currentFilter == FILTER_INACTIVE && !m.isActive());
            boolean queryOk = query.isEmpty()
                    || m.getName().toLowerCase(Locale.ROOT).contains(query)
                    || m.getMemberId().toLowerCase(Locale.ROOT).contains(query);
            if (statusOk && queryOk) result.add(m);
        }
        adapter.submit(result);
    }

    private void updateSummary() {
        int active = 0;
        for (Member m : allMembers) if (m.isActive()) active++;
        totalMembers.setText(String.valueOf(allMembers.size()));
        activeMembers.setText(String.valueOf(active));
    }
}