# SMTP & Python Email Notes

---

## 1. What is smtplib?

`smtplib` is a **built-in Python library** — no pip install needed. It lets you send emails via an SMTP server.

### Core Steps

```python
import smtplib

# 1. Connect
server = smtplib.SMTP(host='smtp.gmail.com', port=587)

# 2. Encrypt the connection
server.starttls()

# 3. Authenticate
server.login('your@gmail.com', 'your_app_password')

# 4. Send
server.send_message(msg)

# 5. Close
server.quit()
```

> **Gmail requires an App Password**, not your real password.
> Go to: Google Account > Security > 2-Step Verification > App Passwords

### Use `with` for Safety
```python
with smtplib.SMTP('smtp.gmail.com', 587) as server:
    server.starttls()
    server.login(email, password)
    server.send_message(msg)
# Connection closes automatically
```

---

## 2. Why Do We Need a Server?

Email doesn't go directly from your computer to the recipient. It follows a chain:

```
Your Python Script
      |
      v
  SMTP Server (e.g. Gmail's smtp.gmail.com)
      |
      v
  Recipient's Mail Server
      |
      v
  Recipient's Inbox
```

### The SMTP Server is the "Post Office"

Think of it like mailing a letter:
- You don't drive to the recipient's house yourself
- You hand the letter to a **post office** (SMTP server)
- The post office handles routing, delivery, and retries

### Why Can't You Send Directly?

| Problem | Why |
|--------|-----|
| **Trust** | Most mail servers reject email from unknown IPs (spam prevention) |
| **Deliverability** | Gmail's servers are whitelisted and trusted by other mail servers |
| **Authentication** | The server verifies you own the "From" address |
| **Always-on** | The recipient's server might be temporarily down — SMTP servers queue and retry |

---

## 3. What is a Network Protocol?

A **protocol** is a set of agreed-upon rules for how two parties communicate.

### Common Protocols

| Protocol | Stands For | Used For |
|----------|-----------|---------|
| **HTTP** | HyperText Transfer Protocol | Loading websites |
| **HTTPS** | HTTP Secure | Secure websites |
| **SMTP** | Simple Mail Transfer Protocol | **Sending** email |
| **IMAP/POP3** | — | **Reading** email |
| **FTP** | File Transfer Protocol | Transferring files |
| **TCP/IP** | Transmission Control Protocol | Foundation of the internet |

### SMTP Protocol Conversation

```
Your Script         Gmail Server
    |                    |
    |--- "HELO" -------->|   (Hello, I want to connect)
    |<-- "250 OK" -------|   (OK, go ahead)
    |--- "AUTH login" -->|   (I want to log in)
    |<-- "235 OK" -------|   (Authenticated)
    |--- "MAIL FROM" --->|   (Email is from this address)
    |--- "RCPT TO" ----->|   (Send it to this address)
    |--- "DATA" -------->|   (Here is the message content)
    |<-- "250 OK" -------|   (Message accepted)
    |--- "QUIT" -------->|   (Done, goodbye)
```

`smtplib` handles all of this conversation for you automatically.

---

## 4. What is MIMEText and MIMEMultipart?

**MIME** stands for **Multipurpose Internet Mail Extensions**.

Email was originally designed to send plain text only. MIME was invented to extend email so it could carry different types of content (HTML, images, files, etc.).

### MIMEText

A single piece of text content — either plain text or HTML.

```python
from email.mime.text import MIMEText

# Plain text
msg = MIMEText("Hello, this is a plain text email.")

# HTML
msg = MIMEText("<h1>Hello</h1><p>This is HTML</p>", "html")
```

Think of it as **the letter inside the envelope**.

### MIMEMultipart

A container that holds **multiple parts** together — like a text body + attachments.

```python
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

msg = MIMEMultipart()
msg['From'] = 'you@gmail.com'
msg['To'] = 'friend@gmail.com'
msg['Subject'] = 'Hello'

body = MIMEText("Hi, here is your file!")
msg.attach(body)
msg.attach(attachment)
```

Think of it as **the envelope** — it holds everything together.

### Visual Structure

```
MIMEText only (simple email):
┌─────────────────┐
│  Plain Text     │  ← just the letter, no envelope needed
└─────────────────┘

MIMEMultipart (complex email):
┌──────────────────────────────┐
│  MIMEMultipart (envelope)    │
│  ┌────────────────────────┐  │
│  │  MIMEText (body text)  │  │
│  └────────────────────────┘  │
│  ┌────────────────────────┐  │
│  │  MIMEBase (attachment) │  │
│  └────────────────────────┘  │
└──────────────────────────────┘
```

### When to Use Which

| Situation | Use |
|-----------|-----|
| Simple text-only email | `MIMEText` alone |
| Email with attachments | `MIMEMultipart` + `MIMEText` + `MIMEBase` |
| Email with HTML + plain text fallback | `MIMEMultipart('alternative')` + two `MIMEText` parts |

---

## 5. Line-by-Line Explanation of smtp.py

### `setup_server()` — Connect to Gmail

```python
server = smtplib.SMTP(host='smtp.gmail.com', port=587)
```
Opens a connection to Gmail's SMTP server. **Port 587** is the standard port for sending email securely.

```python
server.starttls()
```
Upgrades the connection to **encrypted (TLS)**. Without this, your password and email would travel as plain text — anyone could intercept it.

```python
return server
```
Returns the connected server so other functions can use it.

---

### `login()` — Authenticate

```python
address = input("Sender Email: ").strip()
password = input("Password: ").strip()
```
Asks the user to type their email and password. `.strip()` removes accidental spaces.

```python
server.login(address, password)
```
Authenticates with Gmail — proves you own this account. **Without this, Gmail would reject your emails.**

```python
return address
```
Returns the email address so `create_email()` can use it as the "From" field.

---

### `create_email()` — Build the Email

```python
msg = MIMEMultipart()
```
Creates the email object — a blank envelope that can hold text and attachments.

```python
msg['From'] = address
msg['To'] = recipient_email
msg['Subject'] = input("Enter subject of the message: ").strip()
```
Fills in the email headers — who it's from, who it goes to, and the subject line.

```python
message = input("Enter message: ").strip()
msg.attach(MIMEText(message, 'plain'))  # Fixed: body must be attached
```
Collects the message body and attaches it to the email.

---

### `send()` — Send the Email

```python
server.send_message(msg)
```
Hands the email to Gmail's server to deliver. This is the actual send.

```python
del msg
```
Deletes the email object from memory after sending — cleanup.

---

### `add_attachment()` — Attach a File

```python
file = open(filename, 'rb')
```
Opens the file in **binary read mode** (`rb`) — needed because attachments are raw bytes, not text.

```python
attachment = MIMEBase('application', 'octet-stream')
```
Creates a generic binary attachment container. `octet-stream` means "raw binary file of any type".

```python
attachment.set_payload(file.read())
```
Puts the file's contents into the attachment.

```python
encoders.encode_base64(attachment)
```
Converts the binary file to **Base64**. Email was designed for text, so binary files must be encoded to a text-safe format before sending.

```python
attachment.add_header('Content-Disposition', 'attachment', filename=filename)
```
Tells the recipient's email client that this is a downloadable file and what to name it. See section 6 for full explanation.

```python
msg.attach(attachment)
```
Adds the attachment to the email object.

---

### Main Execution

```python
server = setup_server()     # Connect to Gmail
address = login(server)     # Log in, get sender address
msg = create_email(address) # Build the email
send(server, msg)           # Send it
```

---

## 6. Why We Need `add_header()`

When a file is attached to an email, the email is just **one big block of text** travelling through the internet. The email client on the receiving end needs **instructions** to know what each part is.

### The Analogy

```
Without a label:
┌─────────────────┐
│  ???????????    │  ← receiver has no idea what this is
│  (binary data)  │     or what to do with it
└─────────────────┘

With a label:
┌─────────────────────────────────────┐
│  Content-Disposition: attachment    │  ← "this is a downloadable file"
│  filename: report.pdf               │  ← "and its name is report.pdf"
│─────────────────────────────────────│
│  (binary data)                      │
└─────────────────────────────────────┘
```

### What Each Argument Means

```python
attachment.add_header(
    'Content-Disposition',  # "here is how to display this part"
    'attachment',           # "show it as a downloadable attachment, not inline"
    filename=filename       # "name the file this when the user downloads it"
)
```

| Argument | Meaning |
|----------|---------|
| `'Content-Disposition'` | The type of instruction (display instruction) |
| `'attachment'` | Don't show inline — offer it as a download |
| `filename=filename` | The name the file gets when downloaded |

### What Happens Without It

Without this header, the email client sees raw binary data with no label. It might:
- Display garbled binary characters in the email body
- Ignore the file completely
- Not know what filename to give it

---

## 7. Bugs in the Original Code

| Issue | Location | Problem | Fix |
|-------|----------|---------|-----|
| `message` body never attached | `create_email()` | Body collected but never added to `msg` | Add `msg.attach(MIMEText(message, 'plain'))` |
| `add_attachment()` never called | `create_email()` while loop | Function exists but is never invoked | Call `add_attachment(msg)` inside the `if attach == 'y'` block |
| Unused import | `send()` | `from email import message` does nothing | Remove it |
| Wrong `add_header()` call | `add_attachment()` | `.strip()` misplaced, wrong arguments | Use `attachment.add_header('Content-Disposition', 'attachment', filename=filename)` |

---

## 8. Key smtplib Methods

| Method | Purpose |
|--------|---------|
| `SMTP(host, port)` | Connect to the mail server |
| `starttls()` | Encrypt the connection (required before login) |
| `login(user, pass)` | Authenticate |
| `send_message(msg)` | Send a `MIMEText`/`MIMEMultipart` message |
| `quit()` | Close the connection |
