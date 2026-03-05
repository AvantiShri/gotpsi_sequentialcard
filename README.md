# gotpsi_sequentialcard
Repository for code for the Got Psi sequential card test

## Data headaches

Av is making a log of data headaches encountered so far

### Missing days

For the data in the zip file `cardS16.zip`, which contains data from 2002 to 2018, the data from Jan to June is hiding in the zip files cardS02Q1.zip and cardS02Q2.zip. I added in code to unzip those. After taking that into account, data is still missing for the following date ranges in 2015-2016:
```
  2015-08-13 to 2015-09-20  (39 days)
  2015-09-24 to 2015-09-27  (4 days)
  2015-09-29 to 2015-10-03  (5 days)
  2015-10-07 to 2015-10-09  (3 days)
  2015-10-11 to 2015-10-26  (16 days)
  2015-12-04 to 2016-05-12  (161 days)
```
Dean said "some dates are missing because the server (especially in 2015) became corrupted (probably due to webbots or hackers), so then the whole site was transferred to another server, and it took a while to get it working."

### Repeated trial numbers for the same user

In `cardS02/cardS020202.dat`, there are two non-identical sets of 25 trials for the user 'igryphon', e.g.
```
igryphon, 1, 2, 0,2,3,0,0,0, ../../bi/images4/c7.gif, Sat Feb  2 04:21:39 2002
...
igryphon, 25, 1, 0,5,0,0,0,0, ../../bi/images4/c6.jpg, Sat Feb  2 04:25:24 2002
...
igryphon, 1, 6, 0,,2,4,1,5,3, ../../bi/images4/ok.jpg, Sat Feb  2 04:25:53 2002
...
igryphon, 25, 1, 0,3,0,0,0,0, ../../bi/images4/ok.jpg, Sat Feb  2 04:29:12 2002
```
On inspection, it seems that the highest trial number in this file is 25; trials after that just loop back to 1

### Empty click entries

It seems that the server sometimes logs empty clicks without an associated card entry. Here is an example:

```
chrisreed, 7, 4, Sat Feb  2 16:46:19 2002
chrisreed, 7, 3, Sat Feb  2 16:46:21 2002
chrisreed, 7, , Sat Feb  2 16:46:22 2002
chrisreed, 7, 1, Sat Feb  2 16:46:23 2002
chrisreed, 7, 2, Sat Feb  2 16:46:24 2002
chrisreed, 7, 5, Sat Feb  2 16:46:26 2002
chrisreed, 7, 6, 0,4,3,,1,2,5, ../../bi/images4/c7.jpg, Sat Feb  2 16:46:26 2002
```
