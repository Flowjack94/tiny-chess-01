import json,os,sys,urllib.request as R
U=os.environ.get('MAKEFUN_ENV_URL')or sys.exit('no env')
V=(0,100,320,330,500,900,0)
NF=(-33,-31,-18,-14,14,18,31,33)
KF=(-17,-16,-15,-1,1,15,16,17)
BF=(-17,-15,15,17)
RF=(-16,-1,1,16)
DM={4:3,116:12,0:2,7:1,112:8,119:4}
# pawn table (white view, rank1..rank8 rows): centre push, big near promotion
PS='kkkkkkkkkkkkkkkkkkkllkkkkklmmlkkklmoomlkklnqqnlkqqqqqqqqkkkkkkkk'
# knight table: centre outposts
NS='kkkkkkkkkkkllkkkkkmmmmkkklmnnmlkkkmnnmkkkkmmmmkkkkkllkkkkkkkkkkk'
C=tuple(int(4-max(abs(i%8-3.5),abs(i//8-3.5)))for i in range(64))
E=[(0,)*64]
E+=[tuple(V[p]+(ord(c)-107)*5 for c in s)for p,s in((1,PS),(2,NS))]
E+=[tuple(V[p]+C[i]*w for i in range(64))for p,w in((3,3),(4,2),(5,1),(6,-3))]
B=[0]*128
KS=[4,116]
T=1
CR=15
EP=-1
UD=[]
KL=[0]*256
HS={}
ND=[0]
BU=100000
M=1000000
PB=(0,0,8,18,35,60,90,130)
TT={};GH=set();PC=[0,0]
class A(Exception):pass
def att(s,c):  # is square s attacked by colour c?
    if c>0:  # white attacker
        for t in(s-15,s-17):  # white pawn capture squares
            if not(t&136)and B[t]==1:return 1  # white pawn attacks
    else:  # black attacker
        for t in(s+15,s+17):  # black pawn capture squares
            if not(t&136)and B[t]==-1:return 1  # black pawn attacks
    for d in NF:  # knight jumps
        t=s+d  # knight target square
        if not(t&136)and B[t]==2*c:return 1
    for d in KF:
        t=s+d
        if not(t&136)and B[t]==6*c:return 1
    for d in BF:
        t=s+d
        while not(t&136):
            q=B[t]
            if q:
                if q==3*c or q==5*c:return 1
                break
            t+=d
    for d in RF:
        t=s+d
        while not(t&136):
            q=B[t]
            if q:
                if q==4*c or q==5*c:return 1
                break
            t+=d
    return 0
def gen():
    ms=[]
    for f in range(128):
        if f&136:continue
        p=B[f]
        if not p or(p>0)!=(T>0):continue
        a=p if p>0 else-p
        if a==1:
            d=16 if p>0 else-16
            t=f+d
            if B[t]==0:
                if(t>>4)==(7 if p>0 else 0):
                    for r in(5,4,3,2):ms.append(f|(t<<7)|(r<<14))
                else:
                    ms.append(f|(t<<7))
                    if(f>>4)==(1 if p>0 else 6)and B[f+2*d]==0:ms.append(f|((f+2*d)<<7))
            for t in(f+d-1,f+d+1):
                if t&136:continue
                q=B[t]
                if q and(q>0)!=(p>0)and abs(q)!=6:
                    if(t>>4)==(7 if p>0 else 0):
                        for r in(5,4,3,2):ms.append(f|(t<<7)|(r<<14))
                    else:ms.append(f|(t<<7))
                elif t==EP:ms.append(f|(t<<7))
        elif a==2 or a==6:
            for d in(NF if a==2 else KF):
                t=f+d
                if t&136:continue
                q=B[t]
                if q==0:ms.append(f|(t<<7))
                elif(q>0)!=(p>0)and abs(q)!=6:ms.append(f|(t<<7))
        else:
            for d in(BF if a==3 else RF if a==4 else KF):
                t=f+d
                while not(t&136):
                    q=B[t]
                    if q==0:ms.append(f|(t<<7))
                    else:
                        if(q>0)!=(p>0)and abs(q)!=6:ms.append(f|(t<<7))
                        break
                    t+=d
    if T>0:
        if CR&1 and B[5]==0 and B[6]==0 and B[7]==4 and not att(4,-1)and not att(5,-1)and not att(6,-1):ms.append(4|(6<<7))
        if CR&2 and B[3]==0 and B[2]==0 and B[1]==0 and B[0]==4 and not att(4,-1)and not att(3,-1)and not att(2,-1):ms.append(4|(2<<7))
    else:
        if CR&4 and B[117]==0 and B[118]==0 and B[119]==-4 and not att(116,1)and not att(117,1)and not att(118,1):ms.append(116|(118<<7))
        if CR&8 and B[115]==0 and B[114]==0 and B[113]==0 and B[112]==-4 and not att(116,1)and not att(115,1)and not att(114,1):ms.append(116|(114<<7))
    return ms
def make(m):
    global T,CR,EP
    f=m&127;t=(m>>7)&127;r=m>>14
    p=B[f]
    if abs(p)==1 and t==EP:
        q=-p;c=t-16*p;B[c]=0
    else:
        q=B[t];c=t
    UD.append((m,q,c,CR,EP))
    B[t]=(r if p>0 else-r)if r else p
    B[f]=0
    if abs(p)==6:
        KS[0 if p>0 else 1]=t
        if abs(t-f)==2:
            if t==6:B[5]=4;B[7]=0
            elif t==2:B[3]=4;B[0]=0
            elif t==118:B[117]=-4;B[119]=0
            else:B[115]=-4;B[112]=0
    CR&=~DM.get(f,0)
    CR&=~DM.get(t,0)
    EP=f+16*p if abs(p)==1 and abs(t-f)==32 else-1
    if q and 1<abs(q)<6:PC[0 if q>0 else 1]-=1
    if r:PC[0 if p>0 else 1]+=1
    T=-T
def unmake():
    global T,CR,EP
    m,q,c,cr,ep=UD.pop()
    f=m&127;t=(m>>7)&127;r=m>>14
    p=B[t]
    B[f]=(1 if p>0 else-1)if r else p
    if c==t:B[t]=q
    else:B[t]=0;B[c]=q
    if abs(p)==6:
        KS[0 if p>0 else 1]=f
        if abs(t-f)==2:
            if t==6:B[7]=4;B[5]=0
            elif t==2:B[0]=4;B[3]=0
            elif t==118:B[119]=-4;B[117]=0
            else:B[112]=-4;B[115]=0
    CR,EP=cr,ep
    if q and 1<abs(q)<6:PC[0 if q>0 else 1]+=1
    if r:PC[0 if p>0 else 1]-=1
    T=-T
def ev():
    s=0;wb=bb=0;wq=bq=0;wp=[9]*8;bp=[0]*8;wfc=[0]*8;bfc=[0]*8;wps=[];bps=[]
    wro=[];bro=[]
    for q in range(128):
        if q&136:continue
        p=B[q]
        if not p:continue
        i=(q>>4)*8+(q&7);r=q>>4;f=q&7
        if p>0:
            s+=E[p][i]
            if p==3:wb+=1
            if p==5:wq=1
            if p==1:
                wps.append((r,f));wfc[f]+=1
                if r<wp[f]:wp[f]=r
            if p==4:wro.append((r,f))
        else:
            s-=E[-p][i^56]
            if p==-3:bb+=1
            if p==-5:bq=1
            if p==-1:
                bps.append((r,f));bfc[f]+=1
                if r>bp[f]:bp[f]=r
            if p==-4:bro.append((r,f))
    if wb==2:s+=30
    if bb==2:s-=30
    for f in range(8):
        if wfc[f]>1:s-=12*(wfc[f]-1)
        if bfc[f]>1:s+=12*(bfc[f]-1)
        if wfc[f] and not(wfc[max(0,f-1)] if f>0 else 0)and not(wfc[min(7,f+1)] if f<7 else 0):s-=10
        if bfc[f] and not(bfc[max(0,f-1)] if f>0 else 0)and not(bfc[min(7,f+1)] if f<7 else 0):s+=10
    for r,f in wps:
        if bp[max(0,f-1)]<=r and bp[f]<=r and bp[min(7,f+1)]<=r:s+=PB[r]
    for r,f in bps:
        if wp[max(0,f-1)]>=r and wp[f]>=r and wp[min(7,f+1)]>=r:s-=PB[7-r]
    for r,f in wro:
        if not wfc[f] and not bfc[f]:s+=18
        elif not wfc[f]:s+=8
        if r==6:s+=22
    for r,f in bro:
        if not wfc[f] and not bfc[f]:s-=18
        elif not bfc[f]:s-=8
        if r==1:s-=22
    for k,sg in((KS[0],1),(KS[1],-1)):
        r=k>>4;f=k&7;sh=0
        for df in(-1,0,1):
            nf=f+df
            if 0<=nf<8:
                t=(r+sg)*16+nf
                if 0<=t<128 and B[t]==sg:sh+=1
        s+=sg*(sh-1)*15
    if not wq and not bq:
        s+=6*(C[(KS[0]>>4)*8+(KS[0]&7)]-C[(KS[1]>>4)*8+(KS[1]&7)])
    return s if T>0 else-s
def sc(m,pl):
    t=(m>>7)&127
    v=B[t]
    if v==0 and t==EP:v=1
    s=10*V[abs(v)]-V[abs(B[m&127])]//10 if v else 0
    if m>>14:s+=900
    if pl>127:pl=127
    if m==KL[pl*2]:s+=600
    elif m==KL[pl*2+1]:s+=400
    h=HS.get(m)
    if h:s+=h if h<400 else 400
    return s
def qs(a,b,pl):
    ND[0]+=1
    if ND[0]>BU:raise A
    if pl>110:return ev()
    ch=att(KS[T<0],-T)
    if ch:best=-M-1
    else:
        best=ev()
        if best>=b:return b
        if best>a:a=best
    n=0
    cm=[]
    for m in gen():
        t=(m>>7)&127
        if not ch and B[t]==0 and not(m>>14)and t!=EP:continue
        cm.append(m)
    cm.sort(key=lambda m:sc(m,pl),reverse=True)
    for m in cm:
        t=(m>>7)&127
        if not ch and not(m>>14):
            v=B[t];cv=V[abs(v)]if v else 100 if t==EP else 0
            if best+cv+100<a:continue
        make(m)
        if att(KS[T>0],T):
            unmake();continue
        n+=1
        s=-qs(-b,-a,pl+1)
        unmake()
        if s>best:best=s
        if s>=b:return b
        if s>a:a=s
    if ch and n==0:return-M+pl
    return a
def sr(a,b,d,pl):
    global T,EP
    ND[0]+=1
    if ND[0]>BU:raise A
    if pl>90:return ev()
    ch=att(KS[T<0],-T)
    if d<=0:
        if ch:d=1
        else:return qs(a,b,pl)
    K=(tuple(B),T,CR,EP)
    if K in GH:return 0
    e=TT.get(K);hm=0
    if e and e[0]>=d:
        s=e[1]
        if s>M-1000:s+=pl
        elif s<-M+1000:s-=pl
        if e[2]==0:return s
        if e[2]==1 and s>=b:return s
        if e[2]==2 and s<=a:return s
        hm=e[3]
    ao=a
    if not ch:
        if d>=3 and PC[0 if T>0 else 1]:
            T=-T;e2=EP;EP=-1
            try:s=-sr(-b,-b+1,d-4 if d>=6 else d-3,pl+1)
            except A:
                T=-T;EP=e2;raise
            T=-T;EP=e2
            if s>=b:return b
    ms=gen()
    ms.sort(key=lambda m:sc(m,pl),reverse=True)
    if hm and hm in ms:
        ms.remove(hm);ms.insert(0,hm)
    n=0;bm=0
    for i,m in enumerate(ms):
        t=(m>>7)&127;cap=B[t];pr=m>>14
        make(m)
        if att(KS[T>0],T):
            unmake();continue
        n+=1
        if i>=4 and d>=3 and cap==0 and not pr and not ch:
            r=3 if i>=8 else 2
            s=-sr(-a-1,-a,d-1-r,pl+1)
            if s>a:s=-sr(-b,-a,d-1,pl+1)
        else:
            s=-sr(-b,-a,d-1,pl+1)
        unmake()
        if s>=b:
            if cap==0 and not pr:
                KL[pl*2+1]=KL[pl*2];KL[pl*2]=m
                HS[m]=HS.get(m,0)+d*d
            sv=b
            if sv>M-1000:sv-=pl
            elif sv<-M+1000:sv+=pl
            TT[K]=(d,sv,1,m)
            if len(TT)>250000:TT.clear()
            return b
        if s>a:a=s;bm=m
    if n==0:return-M+pl if ch else 0
    sv=a
    if sv>M-1000:sv-=pl
    elif sv<-M+1000:sv+=pl
    TT[K]=(d,sv,2 if a<=ao else 0,bm)
    if len(TT)>250000:TT.clear()
    return a
def root():
    global BU
    ND[0]=0
    ms=gen()
    if not ms:return None
    if len(ms)==1:return ms[0]
    ph=0
    for x in B:
        if 1<abs(x)<6:ph+=V[abs(x)]
    BU=80000 if ph>2800 else 50000 if ph<1400 else 65000
    if len(ms)==2:BU=40000 if BU>40000 else BU
    ms.sort(key=lambda m:sc(m,0),reverse=True)
    bb=ms[0]
    for d in range(1,11):
        try:
            a=-M;bs=-M-1;nb=bb
            for m in ms:
                make(m)
                if att(KS[T>0],T):
                    unmake();continue
                s=-sr(-M,-a,d-1,1)
                unmake()
                if s>bs:bs=s;nb=m
                if s>a:a=s
            bb=nb
            ms.remove(bb);ms.insert(0,bb)
        except A:
            while UD:unmake()
            break
    return bb
def load(f):
    global T,CR,EP
    p=f.split()
    B[:]=[0]*128
    r=7;g=0
    for c in p[0]:
        if c=='/':r-=1;g=0
        elif c.isdigit():g+=int(c)
        else:
            v='PNBRQK'.index(c.upper())+1
            B[r*16+g]=v if c.isupper() else-v
            if v==6:KS[0 if c.isupper()else 1]=r*16+g
            g+=1
    T=1 if p[1]=='w' else-1
    CR=(1 if'K'in p[2]else 0)|(2 if'Q'in p[2]else 0)|(4 if'k'in p[2]else 0)|(8 if'q'in p[2]else 0)
    EP=-1 if p[3]=='-'else(ord(p[3][0])-97)+(int(p[3][1])-1)*16
    PC[0]=PC[1]=0
    for x in B:
        if 1<x<6:PC[0]+=1
        elif -6<x<-1:PC[1]+=1
    UD.clear()
def uci(m):
    f=m&127;t=(m>>7)&127
    s=chr(97+(f&7))+str((f>>4)+1)+chr(97+(t&7))+str((t>>4)+1)
    return s+('nbrq'[(m>>14)-2]if m>>14 else'')
def post(p,b):
    q=R.Request(U+p,data=json.dumps(b).encode(),headers={'content-type':'application/json'})
    with R.urlopen(q)as r:return json.load(r)
if __name__=='__main__':
    while True:  # play games until the server says done
        g=post('/game',{})  # fetch next game state
        GH.clear();TT.clear();HS.clear()  # fresh search tables
        if g['status']=='done':break  # tournament over
        while g['status']=='your_move':  # our turn to move
            load(g['fen'])  # set up the board
            GH.add((tuple(B),T,CR,EP))  # repetition guard
            mv=root()  # search the best move
            u=uci(mv)if mv is not None else g['legal_moves'][0]  # move in UCI
            if u not in g['legal_moves']:u=g['legal_moves'][0]
            g=post('/move',{'game':g['game'],'move':u})
        print('game',g['game'],g.get('outcome'),g.get('reason'),file=sys.stderr)
    print('done',g.get('wins'),g.get('draws'),g.get('losses'),file=sys.stderr)
