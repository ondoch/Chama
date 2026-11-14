package com.example.ch_admin;

import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.widget.TextView;

import androidx.annotation.NonNull;
import androidx.recyclerview.widget.RecyclerView;

import java.util.ArrayList;
import java.util.List;

public class MemberAdapter extends RecyclerView.Adapter<MemberAdapter.VH> {

    private final List<Member> items = new ArrayList<>();

    public void submit(List<Member> newItems) {
        items.clear();
        items.addAll(newItems);
        notifyDataSetChanged();
    }

    @NonNull
    @Override
    public VH onCreateViewHolder(@NonNull ViewGroup parent, int viewType) {
        View v = LayoutInflater.from(parent.getContext())
                .inflate(R.layout.item_member, parent, false);
        return new VH(v);
    }

    @Override
    public void onBindViewHolder(@NonNull VH h, int position) {
        Member m = items.get(position);
        h.tvInitials.setText(initialsOf(m.getName()));
        h.tvName.setText(m.getName());
        h.tvMemberId.setText(m.getMemberId());

        if (m.isActive()) {
            h.tvStatus.setText(R.string.active);
            h.tvStatus.setBackgroundResource(R.drawable.bg_status_active);
            h.tvStatus.setTextColor(0xFF1E9E57);
        } else {
            h.tvStatus.setText(R.string.inactive);
            h.tvStatus.setBackgroundResource(R.drawable.bg_status_inactive);
            h.tvStatus.setTextColor(0xFF1F1B4D);
        }
    }

    @Override
    public int getItemCount() { return items.size(); }

    private static String initialsOf(String name) {
        String[] parts = name.trim().split("\\s+");
        if (parts.length == 0 || parts[0].isEmpty()) return "?";
        String first = parts[0].substring(0, 1);
        String last = parts.length > 1 ? parts[parts.length - 1].substring(0, 1) : "";
        return (first + last).toUpperCase();
    }

    static class VH extends RecyclerView.ViewHolder {
        final TextView tvInitials, tvName, tvMemberId, tvStatus;

        VH(@NonNull View itemView) {
            super(itemView);
            tvInitials = itemView.findViewById(R.id.tvInitials);
            tvName = itemView.findViewById(R.id.tvName);
            tvMemberId = itemView.findViewById(R.id.tvMemberId);
            tvStatus = itemView.findViewById(R.id.tvStatus);
        }
    }
}