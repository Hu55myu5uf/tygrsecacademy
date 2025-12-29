# TygrSecAcademy Security Documentation

## Overview

TygrSecAcademy implements multiple layers of security to protect user data, prevent unauthorized access, and ensure platform integrity. As a cybersecurity education platform, security is our highest priority.

## Authentication Architecture

### JWT Token-Based Authentication

We use JSON Web Tokens (JWT) for stateless authentication:

**Token Types:**
- **Access Token**: Short-lived (15 minutes), used for API requests
- **Refresh Token**: Long-lived (7 days), used to obtain new access tokens

**Token Storage:**
- Tokens stored in HTTP-only cookies (frontend)
- Refresh tokens also stored in database with revocation capability
- Access tokens include user ID and role in payload

**Token Flow:**
1. User logs in with email/password
2. Server validates credentials and creates access + refresh tokens
3. Tokens sent to client and stored
4. Client includes access token in Authorization header for API requests
5. When access token expires, client uses refresh token to get new one
6. On logout, refresh token is revoked in database

### Password Security

**Hashing:**
- bcrypt algorithm with cost factor 12
- Passwords never stored in plain text
- Password hashes never exposed via API

**Password Requirements:**
- Minimum 8 characters
- At least one uppercase letter
- At least one lowercase letter
- At least one digit
- At least one special character (!@#$%^&*()_+-=[]{}|;:,.<>?)

**Password Reset:**
- Secure token-based reset flow
- Reset tokens expire after 1 hour
- One-time use tokens (invalidated after reset)

## Role-Based Access Control (RBAC)

### User Roles

1. **Student**
   - Access curriculum and lessons
   - Start and complete labs
   - Submit challenge flags
   - View own progress
   - Submit capstones
   - Publish approved content

2. **Tutor**
   - All student permissions
   - View student progress
   - Review capstone projects
   - Provide feedback
   - Approve publications

3. **Admin**
   - All tutor permissions
   - Manage users (create, update, delete)
   - Manage curriculum (modules, lessons, labs)
   - Configure challenges
   - View platform analytics
   - Access audit logs

### Permission Enforcement

**Backend:**
- Route-level permission checks using decorators
- `@require_student()`, `@require_tutor()`, `@require_admin()`
- User loaded from JWT token on every request
- Role verified before executing operation

**Frontend:**
- Conditional rendering based on user role
- Route guards prevent navigation to unauthorized pages
- API calls fail gracefully if permissions insufficient

## Data Encryption

### In Transit
- **HTTPS Only** in production (enforced via middleware)
- TLS 1.2+ required
- Strong cipher suites only
- HSTS headers (max-age=31536000)

### At Rest
- Database uses PostgreSQL native encryption
- Sensitive fields (e.g., refresh tokens) hashed
- File uploads scanned and stored securely

## SQL Injection Prevention

**SQLAlchemy ORM:**
- All database queries use parameterized statements
- ORM prevents direct SQL insertion
- Input validation on all user-provided data

**Example Safe Query:**
```python
user = db.query(User).filter(User.email == email).first()
```

**Never:**
```python
# UNSAFE - Never do this
db.execute(f"SELECT * FROM users WHERE email = '{email}'")
```

## Cross-Site Scripting (XSS) Protection

**Backend:**
- Input sanitization on all user inputs
- Content-Type headers properly set
- X-Content-Type-Options: nosniff
- X-XSS-Protection headers

**Frontend:**
- React automatically escapes rendered content
- Dangerous HTML rendering explicitly marked
- User-generated markdown sanitized before display

## Cross-Site Request Forgery (CSRF) Protection

**Stateless Tokens:**
- JWT tokens in Authorization headers
- Not susceptible to CSRF (no cookies for state-changing operations)

**SameSite Cookies:**
- Cookies set with SameSite=Strict
- Prevents cross-origin cookie sending

## Rate Limiting

**Authentication Endpoints:**
- Login: 5 attempts per minute per IP
- Registration: 3 attempts per minute per IP
- Password reset: 3 attempts per hour per email

**AI Endpoints:**
- 50 requests per user per hour
- Prevents API quota abuse
- Configurable per deployment

**General API:**
- 60 requests per minute per user
- Burst allowance: 10 requests

## Audit Logging

### What We Log

**Security Events:**
- All login attempts (success and failure)
- Password changes
- Failed authorization attempts
- Suspicious activity patterns
- Account modifications

**User Actions:**
- Lesson views
- Lab starts and completions
- Challenge submissions
- Capstone submissions
- Content publications

**Logged Data:**
- User ID
- Action type
- Resource accessed
- IP address
- User agent
- Timestamp
- Success/failure status
- Error messages (if applicable)

### Log Retention

- Audit logs: 1 year
- Security events: 2 years
- Debug logs: 30 days

### Log Access

- Admin-only access to full audit logs
- Users can view own activity log
- Logs stored securely with integrity checks

## API Security

**Headers:**
```
X-Content-Type-Options: nosniff
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
Strict-Transport-Security: max-age=31536000; includeSubDomains
```

**CORS:**
- Explicit origin whitelist
- No wildcards in production
- Credentials: true only for trusted origins

**Input Validation:**
- Pydantic models validate all inputs
- Type checking enforced
- Length limits on all strings
- Email validation
- URL validation

## File Upload Security

**Allowed Extensions:**
- Documents: pdf, md, txt
- Images: png, jpg, jpeg
- Code: py, js, html, css

**Validation:**
- File type verification (not just extension)
- Maximum file size: 10MB
- Virus scanning (optional, recommended)
- Unique filename generation
- Isolated storage directory

## Database Security

**Connection:**
- SSL/TLS for database connections
- Connection pooling with limits
- Credentials in environment variables (never hardcoded)

**Backups:**
- Automated daily backups
- Encrypted backup storage
- Tested restore procedures

**Access:**
- Principle of least privilege
- Application-specific database user
- No direct database access for users

## Secrets Management

**Environment Variables:**
- All secrets in `.env` file
- `.env` never committed to version control
- `.env.example` template provided
- Different secrets per environment

**Secret Rotation:**
- JWT keys rotated every 90 days
- Database passwords rotated every 6 months
- API keys monitored for exposure

## Security Best Practices for Deployment

1. **Use HTTPS Only**
   - Obtain SSL certificate (Let's Encrypt recommended)
   - Redirect all HTTP to HTTPS
   - Enable HSTS

2. **Secure Environment Variables**
   - Use secret management service (AWS Secrets Manager, etc.)
   - Never log secrets
   - Rotate regularly

3. **Database Hardening**
   - Enable SSL connections
   - Use strong passwords
   - Limit network Access
   - Regular security updates

4. **Application Updates**
   - Keep dependencies updated
   - Monitor security advisories
   - Apply patches promptly

5. **Monitoring**
   - Enable security event alerting
   - Monitor for unusual patterns
   - Review logs regularly

6. **Backup and Recovery**
   - Automated backups
   - Test disaster recovery
   - Document procedures

## Incident Response

### If Security Breach Suspected

1. **Immediate Actions:**
   - Isolate affected systems
   - Revoke compromised credentials
   - Enable additional logging

2. **Investigation:**
   - Review audit logs
   - Identify scope of breach
   - Determine attack vector

3. **Remediation:**
   - Patch vulnerabilities
   - Reset affected account passwords
   - Inform affected users

4. **Prevention:**
   - Update security controls
   - Implement additional monitoring
   - Document lessons learned

## Security Checklist for Production

- [ ] HTTPS enabled with valid certificate
- [ ] Secure environment variables configured
- [ ] Database SSL connections enabled
- [ ] Rate limiting configured
- [ ] CORS properly restricted
- [ ] Security headers enabled
- [ ] Audit logging active
- [ ] Backups automated and tested
- [ ] Secrets rotated from defaults
- [ ] Debug mode disabled
- [ ] Error messages sanitized
- [ ] File upload restrictions enforced
- [ ] Monitoring and alerting configured

## Reporting Security Issues

If you discover a security vulnerability in TygrSecAcademy:

1. **Do NOT** open a public issue
2. Email security concerns to security@tygrsecacademy.com
3. Provide detailed description and reproduction steps
4. Allow reasonable time for fixes before disclosure

We take security seriously and appreciate responsible disclosure.
