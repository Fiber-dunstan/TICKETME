# TicketMe — Presentation Outline 

This outline explains every technical term the first time it's used, so
the presentation makes sense to both technical and non-technical audiences.

---

## Slide 1: Title

**TicketMe — A Smart, Automatic Event Registration System**
Built by Dunstan Banyaa
Azubi Africa AWS Cloud & AI Intensive Program — Final Capstone Project

Live demo link: https://d24m8nf71z49d9.cloudfront.net

---

## Slide 2: The Problem — What Was Broken Before

Imagine a company hosting an event. Right now, they might collect signups
using a **Microsoft Form** (an online questionnaire), and all the answers
get dumped into an **Excel spreadsheet** (a table of rows and columns,
like a digital notebook).

This causes real problems:
- Someone has to manually check the spreadsheet to see if a seat is
  still available — there's no automatic "sorry, we're full" message.
- The same person can accidentally sign up twice, and nobody notices.
- No one gets an automatic confirmation email — someone has to send it
  by hand, or nobody does.
- If something breaks, there's no way to know until a customer complains.

**In short: it's slow, manual, and easy to get wrong.**

---

## Slide 3: The Solution — What I Built Instead

TicketMe is a website where people can:
- See a list of upcoming events
- Click "Register" and instantly get a confirmed spot (or a clear
  message if the event is full)
- Look up their own registrations later
- Cancel if they can't make it anymore

Everything happens **automatically, instantly, and correctly** — no
person has to manually check a spreadsheet ever again.

---

## Slide 4: What Does "Serverless" Mean?

You'll hear the word **"serverless"** a lot in this presentation. Here's
what it actually means, in plain terms:

Normally, running a website means renting a computer (called a
**"server"**) that has to stay switched on 24 hours a day, whether
anyone is using your website or not — like leaving a shop open all
night even if no customers come in. You pay for that computer the whole
time, and someone has to maintain it (updates, security, etc.).

**"Serverless" means: there is no computer sitting around waiting.**
Instead, tiny pieces of code wake up **only when someone actually needs
them** (like when someone clicks "Register"), do their job in a
fraction of a second, and then go back to sleep. You only pay for the
exact moments the code actually runs — often close to nothing for a
project like this.

This is provided by **Amazon Web Services (AWS)** — Amazon's cloud
computing platform, which is the leading provider of this kind of
technology.

---

## Slide 5: How the System Works (Step by Step)

Imagine following one person's click of the "Register" button, step by
step, through the system:

1. **Their web browser** sends the registration request over the
   internet.
2. **API Gateway** — think of this as a receptionist at a front desk —
   receives the request and figures out where it needs to go.
3. **AWS Lambda** — a small, specific piece of code that does exactly
   one job (in this case: "register this person") — runs briefly,
   checks everything is valid, and does the work.
4. **DynamoDB** — this is the database, essentially a very fast,
   organized digital filing cabinet — stores the new registration
   permanently.
5. **Amazon SNS (Simple Notification Service)** — a messaging service —
   sends a notification saying "a new registration just happened."
6. The person immediately sees a confirmation on the screen, with their
   own unique ticket code.

All of this happens in under one second.

---

## Slide 6: The Building Blocks We Used

| Technical Term | What It Actually Means |
|---|---|
| **AWS Lambda** | Small pieces of code that run only when needed — like a light that turns on only when you walk into the room, instead of staying on all day. |
| **API Gateway** | The "front door" of the system — it receives requests from the website and passes them to the right piece of code. |
| **DynamoDB** | The database — where all event and registration information is permanently and safely stored. |
| **Amazon SNS** | A messaging system that sends alerts and notifications automatically. |
| **CloudWatch** | A monitoring tool — like a security camera for the system — that watches for anything going wrong and keeps a record (called "logs") of everything that happens. |
| **Terraform** | A tool that lets us describe our entire system as a written document (code), so we can recreate the exact same setup automatically, anytime, instead of manually clicking buttons in a control panel. This is called "Infrastructure as Code." |
| **GitHub Actions** | An automatic checker that tests our code every single time we make a change, to catch mistakes before they cause real problems. |
| **AWS Budgets** | A safety alarm for spending — it emails us if we're about to spend more money than planned. |

---

## Slide 7: Live Demonstration

*(Show the actual website)*

1. Browse the list of events
2. Search for a specific event by name
3. Click "Register," fill in details, submit
4. Show the confirmation with a unique ticket code
5. Go to "My Registrations" and look up that ticket using the same
   email address
6. Cancel the registration and show the seat count update
7. Briefly show the **CloudWatch dashboard** (the monitoring tool) —
   all green, meaning everything is healthy
8. Briefly show **GitHub Actions** — a green checkmark meaning our
   automatic tests passed before this code was allowed to go live

---

## Slide 8: Good Habits We Followed (Why They Matter)

- **We wrote automatic tests** — small programs that check our code
  works correctly, every single time we make a change, without a human
  having to manually click through everything by hand.
- **We gave each piece of code the minimum permission it needs** —
  called "least privilege." For example, the piece of code that only
  needs to *read* the event list is not allowed to *delete* anything —
  even if it were hacked or had a bug, the damage it could do is
  limited.
- **We used version control (Git/GitHub)** — every single change we
  made is recorded, timestamped, and explained, so we (or anyone else)
  can see exactly what changed, when, and why — and undo it if needed.
- **We separated "in-progress" work from "finished, tested" work** —
  using something called **branches**, so unfinished work never
  accidentally goes live before it's ready.

---

## Slide 9: Real Problems We Ran Into (and How We Solved Them)

**Problem:** When someone registered using an email with the `@`
symbol, the system couldn't find their registration afterward.
**Why:** The system was receiving the email address in a slightly
"scrambled" format (a security-related web standard called URL
encoding, where `@` gets temporarily replaced with `%40`), and wasn't
converting it back before searching.
**Fix:** We added a single line of code to "unscramble" it back to
normal before searching — a good reminder to never assume something
works correctly just because it's "supposed to."

**Problem:** Some words we used as data field names (like "capacity"
or "status") turned out to be special reserved words the database
already uses internally — like trying to name your pet "Dog," which
confuses everyone.
**Fix:** We used a workaround the database provides specifically for
this situation.

**Problem:** We occasionally merged unfinished work into the wrong
"branch" (an area for work-in-progress), which caused confusion about
what was actually finished.
**Fix:** We built a checklist habit — checking exactly where we were
before making changes — and used a more precise command-line tool
instead of a webpage button that was easy to click wrong.

---

## Slide 10: Keeping Things Safe (Security)

- No passwords, keys, or secrets are ever written directly into our
  code — they're kept separately and never shared publicly.
- Every piece of code can only touch the exact data it's supposed to —
  nothing more.
- All information sent between the website and our system is encrypted
  (scrambled so nobody else can read it in transit) using **HTTPS**,
  the same padlock-icon security every banking website uses.
- We double-check every single thing a user types in before saving it,
  to block bad or malicious input.

---

## Slide 11: Keeping Costs Low

- We only pay for the exact moments our code runs — not a single cent
  when nobody is using the site.
- We set an automatic spending alarm at $5/month — if AWS ever predicts
  we might spend more than that, we get an email warning immediately.
- We deliberately deleted old log records after 14 days instead of
  keeping them forever, since storing data costs money over time.

---

## Slide 12: What We'd Add Next

- **Real email confirmations sent to each individual person** who
  registers (right now, notifications go to the system operator, not
  the actual attendee — a deliberate, documented limitation for this
  version).
- **QR code tickets** — a scannable barcode-style image for entry.
- **An admin dashboard** — a private area for event organizers to see
  statistics and manage events directly.
- **Smart predictions** — using historical signup data to predict how
  many people are likely to attend future events.

---

## Slide 13: Thank You

Questions welcome.

GitHub repository (all source code): https://github.com/Fiber-dunstan/TICKETME
Live website: https://d24m8nf71z49d9.cloudfront.net