# GitHub API Pagination Analysis

This document explains how GitHub pagination works, how to inspect the `Link` headers, and how to fetch multiple pages manually using `curl`.

---

## 1. What You Are Fetching
When calling:
```
https://api.github.com/users/octocat/repos?page=1&per_page=5
```
you are fetching **public repositories** for the GitHub user **octocat**, limited to **5 repos per page**, starting at **page 1**.

If `page` and `per_page` are omitted:
- `page` defaults to **1**
- `per_page` defaults to **30**

---

## 2. Link Headers
GitHub includes a `Link` header with URLs that allow moving between pages.

Example:
```
Link: <https://api.github.com/users/octocat/repos?page=2&per_page=5>; rel="next",
      <https://api.github.com/users/octocat/repos?page=4&per_page=5>; rel="last"
```

Common `rel` values:
- **next** → the next page
- **prev** → the previous page
- **first** → page 1
- **last** → final page

If `rel="next"` is missing, you're on the last page.

---

## 3. Manual Pagination with curl
### Fetch page 1 including headers:
```
curl -i "https://api.github.com/users/octocat/repos?page=1&per_page=5"
```

### Check only the Link header:
```
curl -I "https://api.github.com/users/octocat/repos?page=1&per_page=5" | grep -i link
```

Copy the URL with `rel="next"` and repeat for the next page.

---

## 4. Finding Total Public Repos
To get the total number of public repositories for a user:
```
curl https://api.github.com/users/octocat
```
Look for the value of:
```
"public_repos": <number>
```

---

Let me know if you want examples added, diagrams, or a JS version next.

