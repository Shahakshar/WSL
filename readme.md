# 🛠️ Developed Ownership Transfer and Revoke Feature

## 📌 PROBLEM 1

In the document, a problem is described in which you have to implement **ownership transfer and revoke functionality**.

For example:  
If user **A** has created or uploaded a document, then that person is the **owner** of that file and also holds **ownership** of the document.  

Now, user A has the right to give ownership to another user — let’s say **B**. After this, **B** becomes the current owner of the file and has the right to **transfer ownership** further.  
This is the exact scenario explained in the problem:  
> A person who currently holds ownership of the document has the right to transfer it, not necessarily the one who originally created it.

---

## 📌 PROBLEM 2

Only the **original creator** of the document has the right to **revoke** ownership.  

They can simply revoke the ownership transfer.  
So even if ownership has been transferred to multiple users, the original creator retains the authority to revoke all transfers.

---

## 📌 PROBLEM 3

Log **every transfer and revoke** action in a **separate database**.

---

## 💡 Intuition and Approach

### ➤ Transfer Logic:
- A creates a file  
  → A is the creator and the current owner.  
- A ➝ B  
  → A gives ownership to B  
  → B becomes the current owner.  
- B ➝ C  
  → B gives ownership to C  
  → C becomes the current owner.

### ➤ Revoke Logic:
- If A revokes the permission, I simply remove the ownership from **all users**.
- But here’s the catch:  
  The question does **not** require maintaining the full chain of ownership transfers.

---

## ✅ Solution Design

I have maintained the entries of:
- `original_owner`
- `ownership`

There are also some other important fields relevant to the revoke case.

The table looks like this:

| file_id | file_name | created_at | original_owner | ownership | ... |

This is the structure I’m thinking of for the given task, which aligns with the provided requirements.
