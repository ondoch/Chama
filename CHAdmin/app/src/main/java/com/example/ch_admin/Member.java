package com.example.ch_admin;

public class Member {
    private final String name;
    private final String memberId;
    private final boolean active;

    public Member(String name, String memberId, boolean active) {
        this.name = name;
        this.memberId = memberId;
        this.active = active;
    }

    public String getName() { return name; }
    public String getMemberId() { return memberId; }
    public boolean isActive() { return active; }
}
