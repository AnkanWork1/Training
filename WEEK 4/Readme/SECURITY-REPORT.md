# SECURITY REPORT — API DEFENSE & INPUT CONTROL (DAY 4)

## Project Context

This report documents the security protections implemented and manually tested for the backend API during **Day 4 — API Defense & Input Control**.

The API is built using:

* Node.js
* Express.js
* MongoDB (Mongoose)

Primary goal:

> Reduce attack surface, validate all inputs, and protect the API against common web vulnerabilities.

---

## Implemented Security Controls

### 1. Input Validation

* Joi validation schemas implemented for:

  * User
  * Product
* Ensures:

  * Correct data types
  * Required fields enforced
  * Malformed payloads rejected early

---

### 2. Payload Whitelisting

* Only validated fields are passed from request body to controllers
* Prevents mass assignment and unexpected field injection

---

### 3. Payload Size Limiting

* Configured using Express body parser

```js
app.use(express.json({ limit: "10kb" }));
```

* Prevents large payload / DoS style attacks

---

### 4. Rate Limiting

* Implemented using `express-rate-limit`
* Configuration:

  * Max requests: **5**
  * Time window: **1 minute**

```js
max: 5
```

* Protects against brute force and abuse

---

### 5. CORS Policy

* Cross-Origin Resource Sharing configured
* Only allowed origins can access API
* Prevents unauthorized cross-origin requests

---

### 6. Helmet Security Headers

* Implemented using `helmet`
* Adds secure HTTP headers such as:

  * X-Content-Type-Options
  * X-Frame-Options
  * Content-Security-Policy
* Protects against:

  * Clickjacking
  * MIME sniffing
  * Reflected XSS

---

### 7. Input Sanitization (XSS Protection)

* Implemented using `xss` library
* Sanitization performed at controller level before database persistence
* Escapes malicious HTML instead of rejecting it

---

## Manual Security Testing

All tests were performed manually using:

* Postman
* MongoDB Compass

---

## Vulnerability Testing & Results

### 1. NoSQL Injection Test

**Payload:**

```json
{
  "email": { "$ne": null },
  "password": "test"
}
```

**Expected Behavior:**

* Request should be rejected due to invalid data type

**Actual Result:**

* Joi validation rejected the request
* API returned `400 Bad Request`

**Status:** ✅ PASS

---

### 2. XSS Injection Test

**Payload:**

```json
{
  "name": "<script>alert('xss')</script>",
  "email": "xss@test.com",
  "password": "Pass1234"
}
```

**Expected Behavior:**

* Script should not execute
* Malicious code should not be stored in executable form

**Actual Result:**

* Input sanitized using `xss`
* Stored value escaped:

  ```
  &lt;script&gt;alert('xss')&lt;/script&gt;
  ```
* No executable script stored in database

**Status:** ✅ PASS

---

### 3. Parameter Pollution Test

**Payload:**

```json
{
  "email": ["user@test.com", "admin@test.com"]
}
```

**Expected Behavior:**

* API should reject invalid data structure

**Actual Result:**

* Joi validation rejected array input
* API returned `400 Bad Request`

**Status:** ✅ PASS

---

### 4. Rate Limiting Test

**Test Method:**

* Sent more than 5 requests within 1 minute from Postman

**Expected Behavior:**

* Requests beyond limit should be blocked

**Actual Result:**

* API returned `429 Too Many Requests`

**Status:** ✅ PASS

---

### 5. Payload Size Limit Test

**Test Method:**

* Sent payload larger than configured size

**Expected Behavior:**

* Request should be rejected

**Actual Result:**

* API returned `413 Payload Too Large`

**Status:** ✅ PASS

---

## Final Security Status

| Security Control           | Status        |
| -------------------------- | ------------- |
| Input Validation           | ✅ Implemented |
| NoSQL Injection Protection | ✅ Safe        |
| XSS Protection             | ✅ Sanitized   |
| Rate Limiting              | ✅ Active      |
| Payload Size Limiting      | ✅ Active      |
| Helmet Headers             | ✅ Active      |
| CORS Policy                | ✅ Enforced    |

---

## Conclusion

The API successfully implements layered security defenses including validation, sanitization, rate limiting, and secure headers. Manual testing confirms resistance against common attacks such as NoSQL Injection, XSS, and parameter pollution.

The system meets all **Day 4 — API Defense & Input Control** deliverables.

---

**Prepared by:**
Ankan Guha
Backend Engineering — Week 4
