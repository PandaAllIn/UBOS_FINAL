---
created: <% tp.date.now("YYYY-MM-DD HH:mm") %>
type: test
---

# Test Note Created at <% tp.date.now("HH:mm") %>

**Date:** <% tp.date.now("dddd, MMMM DD, YYYY") %>

**Test prompt:**
Name: <% tp.system.prompt("What's your name?") %>

**Test suggester:**
Priority: <% tp.system.suggester(["High", "Medium", "Low"], ["high", "medium", "low"]) %>

**Test date math:**
Tomorrow: <% tp.date.now("YYYY-MM-DD", 1) %>
Yesterday: <% tp.date.now("YYYY-MM-DD", -1) %>

---

If you see this with actual dates/values (not template code), Templater is working! ✅
