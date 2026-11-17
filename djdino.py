#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DJ dino RUN 3D
單檔版：Python 標準庫 HTTP 伺服器 + 內嵌 HTML / WebGL 遊戲 / Web Audio 音樂。
不需要額外的 HTML、JS、音訊或 Python 套件檔案。

啟動：
    python3 djdino.py
    python3 djdino.py --port 8080
    python3 djdino.py --kiosk       # Raspberry Pi Chromium 全螢幕
    python3 djdino.py --open        # 自動開啟瀏覽器

排行榜資料會在首次提交分數後寫入同一資料夾的 scores.json。
"""
import argparse
import base64
import json
import os
import shutil
import socket
import subprocess
import sys
import threading
import time
import zlib
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

ROOT = os.path.dirname(os.path.abspath(__file__))
SCORES = os.path.join(os.path.dirname(ROOT), "djdino_scores.json")
LOCK = threading.Lock()

def _unpack(parts):
    return zlib.decompress(base64.b85decode("".join(parts))).decode("utf-8")

HTML = _unpack((
    'c-pO5ZExGw75?sDaYrMoJ&-g>y;zoHVP4{--WtcSoNoPiMP7=xrbvRklB@^@vJD%sc1yM{1D2pe`ekXcei*O}Xa+QYri-2AQ~$!w'
    'xuhuS#ZEdjKtl1pp8K5VJm*}d`2#1k#VBIL6FtAR(!>YxY0%wP?s(d}KU1)cQ3oD9CMdBz8YfI_D}CW=HD%Hq&>q`X2AmC}Fcu22'
    '!$7bAh7GwRylsaKxXm>AqVj+XPJJ!0sn51ewV$w9zR(W52O%yhxbRu)+E0nYgOD8F-Y2DN&5g8mrJ0BkKI?H9im|5Iqxx#8%4)9L'
    '(6nB+zUsOq$2H((<l_r7%g*V_kH($wL`(P`9(3!SFm_;9Xle9l+~q;tXhhU;un#5<S?8DwP0&d5c-Qmcuh8t!597LsX^=!ThSQy{'
    'AX;iCbVg%&w7O{+R~jC};py*iz+%@AhjouT4htF`Y9Dvwupc<}Rb$gAnY58E3ud|v7f{n&+T;GHuC!S<WaRdqqAL5L2uU0ECEyTM'
    'IRGoKgNx+bVc3CQHGy6YfaGo?#gqBW7WE(uSVM$;+ta8mco@i*(-oTr1DcGZFyXS*<tNN(@Bmy3=fB`E4o@PVj_Mshw2x0$^a1Z)'
    'v_ceeAV93K0pOIRW)#jIQwJH)#U~6{W4_O$gb^x;&2XYxfSFV(SJb%Mp=%Y@P%T5%tCe+v7OjI3K%C&aSP@3l=3-RWjjb7rSj4CR'
    'U^SlyjK)*j42N~qRl_idLCol6#xi&(rRW6gSap4xc>gCH()km^3|P$TJM&A4FoK1A=Hhy>bjp;n*1#jB!7%rb>$8)_hy6rwccf*p'
    'SO=pa20Kg)88DFosRNA*)=T7YEfF*pOD&zD<<+nsa~6|*HdNGJ7=&`!bj&a%%cfy81UnI0;!y{<FOjnVssWAHFkBI@#13ONmeU|6'
    'S>5(&FIux|fN*u-sns&T3da>_3~qtP)J==^3IQ`&M(=>rj>k0MJt`sV_(ZQHBoQo1)~t0>I$inkF&nut$W%f){<vaX8RtweE2oG#'
    'U$DjmBUDRAd#ozjlWv_Jqt{(uJf)GJ61x}72kTS0(a@cGdEmju(wSqqlypj6HZ&HDv7|8;8e=U5r<{XR1iC}xOr5fI&`8y+4u+~#'
    'HgKUV#sT_9s*82xbrSmAnYwJElX?xfhG(UH5jLcxE<Jy~IpO0O;h2$>)G(tM4D<1~B?B;DRL$YV_3r>b$3;lNS2Gxl{7bzA-59%3'
    'varY$e!T{`=47dY=0r4L{(OMS&;(w|NG;<Ng~AQvUYav}D%hF^162Gcvnq9Xs(I;zbjfTxqL-5lqaF{|wk&Ykre#RQ(IKU<oWx5t'
    '1`?Dxo{8R_7<8BX#0R()b*~4LMKN`xhsNw$=K^fA7g$)vkT8*irnIAh?$R=s>RXisRvH+xE94Rfo3&J8A)tu`@Z_$R!k@c4Rs1|R'
    'PZ!i|NFH^Bv$3>sA#Z~@F89I8x)X;{#*8(|42S_DQ;k)rs8tgqMAbJd>+588D4+nt<;bc5S!oM~)sT^%Ns=D*{W;DT*i=G5=26<5'
    '3tgmbUWFi0z+hi{BeBaxVi%>xMBM<+bi?nP4^m7F<bz>MB@&!zIaPPTLJKX-I@Jk`t0ig}mVtp4vt%X|OEZy}30Or6VGV__woC|1'
    'm6<HjnC6A3Pt1fcnlKGE2>XKYz{PqLN)IGN05ST;)K$nNQGe{lVQ-pBN|jR)=C3B?6&*&u`AAq;nEDpNSSz4t*K7k0P>eBaDn(nT'
    'E5{utXBrRWxRh`p7g|=v>01CtUfe=rgx5=SJ}ZqeI{Qf-u%6E;^P-=}Or@+^B}>K7(V;?<#n0Om511!H8at+%KCKL{y3BSm(Ga5`'
    'gPR7(U@4{BTh}HRpuLHU6r>nce1g7Ha|~Hzq}IV*WH7N1e~-UIwKaiXhv0{^<kt@&!k+Yk1JxsQQXD}LAwL@_kXB`VYC$L8zcZc_'
    '0~mytu)}azB%AdHvQ?MGPoc<437D-tF4oIvC@LQaUwQp9KFzZyhoS^f=vCMY4FvXjAUPs)Gg5XjK`v4gLKsP(-E(llH0$=Gh{ZO<'
    'I+!m)nutp?wpCr4v463aX6x@)HBkoBGS`?dE0^iIWzFdNr8&Pb^gzy}GZB_yOry#9^~3{qOw~{%#DoGP)k8pXM%qL&F4V}z#np@~'
    '1BkrLuj!lXr)Fh3&AfP;F_~lP=KASoVK4I(GyU6at)-<9#)k+NZnNnn2}-6$7H1d?Gcntx5mvp~eA4N|uwa4ZrlD3;tOKg+OQi5E'
    'brb?^%KQp4zcyh$T$hLmw@7l4e%bvvfn76azm@!!Q4d%gUvwdzz#th@yb5NKHm_!r04&^D!AW_Nt<?$?N2e?a-u$j=AmYu9>?2Nd'
    'Bm2CBpHbkEewiTL*;Z_&)!azmp#v0`K=dRDerM`p7qqmB&G;!`rX3fN_wq^WO5O}NY^AkANONYeyiF=C1OLpe<8h_+?j9+2rAwx3'
    '$T5;}ik#DGAMEa4n_B~JL(t17zp<u6%lN#_c&kxb?c4k9-6L}CaPR%y`9noXe$eb-bLW!*zj$o<1x=X%ChsvR44zs1+SZgcY^y}B'
    'ksk(~Bx;ad__;@p;O{N656+YQ;5#!1V6rBba7ydoaJSti?Sq}GyX5E=X&>zz9?b%ljmPo`?1Vz5B}X?m@F&?Ivgw=O{wZsC_0`jf'
    'Em_Z>Cq4i9*Nf-(V8;2~zrTL?hq+OIOh;vJpG@XF|J}>49yL2LnnTjD2U*|wqc6{X`RU9uH?ywSfBW?H<5@edXI<A1+LQKIpFcal'
    '_xZP9KRW;9DcMHLzy136FP?q$;@QV%Up+ay|MdLcuNTRaWpAamzjJe!G<gtVd75=7q(@JD7IcNTt(b-aI^*}*wsP>^&Ih}PimZ|B'
    'uopopht|+_6_P~E_ic~a$G{irCrnww*tD)tE@BaWzMN$X!CR*?@5FAXv~Hl;x8C19T-*gpZ0dtW81e8{NTu%-B=4QeN;dp1REC6^'
    'ez7RtY(Uf(zJ!3lUU*t-zUNZn9_}6;esBRg5$z{zDLhTQ1{O}c^un}-M}ZA@Znse>Ae81ez^nv|rFkiBfpdNH@E_#n?e^YPatk6c'
    '?Od1&+OM=;Jpb(MufKVD_x`IV&(9uyarWTB`GbF+-~TuHIqTeb@4t6{g#mC#lc)p3N92H$S6_bo^1&D6st30k-tUnY&z_w9<uNwh'
    'IJiyDKKktS-N!gD+bywU9to1f_O?R%4iEJYr7)%Ka|61-<N5xLO!YU?|9<!%>4Jx8'
))
GAME_JS = _unpack((
    'c-pmn|8pD1k?-&PE7nOaSb)G1y8!qNrd*UnNxV=Li=?bmu~hN`SP*LgSa^3q0#sCW$vx-n`10j)=Tw~MBu?U&i=A`6zDoQpN!9yP'
    'Ql`HA7q34(GrO|@NISMqHi6xlo}Qkbo}Qkbo<VLHc}5h6elyP1=S(witX(kf&n+w%YoFntar%?@AHM$IkAL~j>92n{*9`hmY<$UB'
    'GyE3Nw}R%d=k;Uj(2F;^9v&}_H(RFP%GV`u)9oL*5taConQP{f<bfNyJtX(NW8>!T)}H5v&CU*|n%$u3#(vPZB2G;TMgAd5xJUk>'
    '8wa69Ee_WYsZwL!$kBiETHc`R#_b^Nsj^!)Zc$lLEyy)<FXZxIjgjjH$2sGxUp36h+^3M+@eeyW<I7(*7PkEUaAcS+Xj-g()eU<`'
    '`32vKy(l(`v^;>GT3GM5!oY7Wr0EI$m#$nT8i<lP!+6HHZ$wSE>#Z7PYpH1T{QjPLt=8z>9VPF}^xhhTtA<@PTzA!IyWPkuqA_u_'
    'YE%}BM%V9q^k|o<U@+{*tHz@7fNEJyYq7I+Eb3L*62Bwx$KfzVzfw-nJBtZ=yKFqD&&hTjcBxsSqrtpOK|l6J#KU8+aoEiji3YbH'
    '`)=2F2?;U5a$TyZJLqU_368yRC-mB0==GaK67#(@@IrK=OG!E70Ws2V8|G7o-8|tWf%3vIm$#yL-1V%MA5ou=iIQBq>y2`CBlO~7'
    '*sl{KKJzGe`0Bf-@4PFU`z+OQpP1{nNc7AAv;<b$?{>{{zHS5u<vRor9Mr^@EnjVZw-s4NK!g<u3pFtsm_gBK2S>z}Xizlz^pfW)'
    '3`0~Iqo}c9TzBJ+6}x?tfa%pieM!{}FRPC!mvGe;9dSJ&#cX4s<O#s+8zriVvutFQY<{ld*)a-6oBsMbU_v|9#ng9$;2wylE^HQ!'
    'p`yC$#m32quy`P+WHjlkXq=2W#TF?xQcgI<5h)I(boG{Y#)BX>Pev#TV4{Gq7S@bz9mwRviFimV9--nPswp6|M9&UC6OPfC^Thjz'
    '^U4B_@=iEUypK6g;270sku@3t9f}cIBSqFoku}oE61_MEVW1nCB_^CPj6sxm14(EiK~Opf5^o?!lpJOHnO@OjcpUSibBD{|v4Y1k'
    'p14Ct<3t+9{J6-V{J4~WE;Hx}9#<IjB$b?#lT=j7iVT};EScbd=<a!Dg6QaZ<^y-Jkh6+_9&6BJ4SJk~t_tWA4f;fbKFLB)jW8vp'
    'y<rzZN?NC(B$U*OVM1D(qUBBFX`@PC^Yi&MFBEy9$O|ct%c9v$s<}!egs9U!2q7p9kqXM(1DTnm(yJ|UmZx(Zkz+g4S(Q72(-Vz)'
    'kW8>$w>QAB9;pV>#5^L3U7BNDngK?}1*1XF4Lqw-T`%N9C{Z+GF62^eW`hLH%~RcRGVAt&Anv5VBVk!+nu$p;&5<a&ppX;|nmX)M'
    'YsA1xe`bZUp<ZIjOWG0kTdIzP8Xj$-+iwLu6EsQ0sz}Gffa(DHfM%=6+a!J5v7)Zu^h}!5Dnx?42#TCqjVH7$NTq1hJ_dx+mUNIi'
    's_vdYs!THQ09-X))^!d3jH#?lv^mkvCOVwxa3Z0`JoV@&Z#{YK=cjLc<I(rOX_${*{nhD9-#Go<n-72a)6*Znl2?5ayUlx4{dyR>'
    'W2+q!f9?~`{$bpqX}U@RVh95e=GB#M;Kmh)VNGfYaUH@PK>(<SnnQ>=V<eiB?(iZHeJkxq30<FrHlDS_G)U=sZw`i0M=#Crgad<s'
    '%sK_HW1F9k26uE6!9c^HLzYTe$T*bpk4ZwpCu7(bbo*iq`xxJZOAIxihTR&!`WSR0O2SK3WEG6DOjuS4CtPcL*l)r<HNuhU=98fS'
    'O~Mk}3?dWaAE|`M?^8nkT%r^f%mpbC)FAmTXsGK1l6EGVnoxxF9o2PONo^uCl9^2+oD89q^6}?S`N&YboJ}=THDZcOGbtXONASu2'
    'EWuf}PZ2!Ntd1twUs4p0Q;I*ct-056TV9y9d=LhQ=21j8VI(Fmsemy4&6t{=(Z?8dhh3`~dT#6qR3`K+rA7R<7YsvEY#kKj<Yv$t'
    '_+14{t1Uws*|6nBDzD4D7}-S>xpd?D&gRy}-M#(w{hNFFyb*W8;Fy)oMi>U6sTbbtw}UNeLMNY21sxtoswo4V<{fG-)n*Ff+?Ymu'
    'N76>7aqk{*KfAHJzwu9Z_pYs9-q<Y~M^XMf=qtPHSFdku?<eqW1yAdmd#b(x8_-(QWk%Ze0k?f?bNeeF*Kk=>wS17zr;QzA_3)rB'
    '-}<8IXIHm=X@B$Cjk`CuH?Q2-y}rkYX32JcLbm(81oJw{(UEtv?_((iw0_>|QzdmWaQnSG37mx3lB;h(_Ipt3bBXnF-=M@H`tE_$'
    'y*s-bmk7gib6@n^Ew61{-MX9b8+n_1n>V)aUfaBSZEg^HO+SK2V{JDu+L)K>b6@mm1*m2Ayp})gY1#dj-=2F;Df{aid)Kg%$EbL2'
    'j(R-w8^hQ$j=W~YaCZV4DDHL;QsYE(Xqg*Vjp4I9MELcf<#p2>E;8KnPly#qZaDV)ha&B0n}q6CeeQ@B@>HHwO8!1_s>U&v2#ltH'
    'cM}yB7)8;xh*w9q){d<ajOL^5H8TTAL>0?cJ}<HlyLYLm4@R#MafM^z^K->HX6HPya~3@lgkK7}gmQSv?G=Yx#L>7o+`Bg}4zGr^'
    'MsF2|SAxUhaM$k<Tw0X5Y794ee#Ds!cDXoQ$8tQ|V(NCTsK3_78oW!5G>^8STNy`dt>=!+7OjN(vi>~US69W{USo}{Br~B0#PzLl'
    '!K%$$wG^(oCR$Q3sYJnAbmm*&SjDuhqP0>fTFbROC8q_B*3jk>7$Pb0qj*hNKjslSVPOqPJX9DU^m}WA;FvI$QksvL+@eFM3*bb-'
    'TH;YUzb2VhpkniqHfC6gu)Rj8ywSicG5ZRPm8vW)THMD(8MU33>4kQ|w(J@U2aq#Inxb#ooJ4|fC3FwDnl+Y`rtA&Me(+pk?CyQ#'
    '_8DUDkl1Gg*fEZfkP+UUH2~>SC*_xTys{#M_bdSv_$DN1JsK2;*C2rVe$Oiow}k{=BpptIm62742HCJbDZcxGKyayu+;#rENX8YT'
    '?>M%}B?m;jR6gy{ZNj70=MEeck#E}0l4Tbwwrwrt^Z7!xvQ%5PYSmhW71x9~OWbQmJJz^_x|IaQYhn%4S%8cn2g0FxO^9jG72+&N'
    '2K5lBxJa_Bpd1<$OqEGBj7n&cH6rN(uSA_l87D(1R8rf@r?PdA^ag{KP$a)V%uMo{!+0%<y@5%@-OCsFQLyD+VUY+aie}uC#1}Aj'
    '($XZM%{8%{<C4Q&>Zy`dww+>_FQDawKW%X&q*d!3g<cF{S&5w6x-@P8Q{Z6{7I<8lR;@PAGEuOcTFRzqAov6}rR>QUYBj4aApF)E'
    '5lu5{G)UPMu0bw*om;db2n9>5l_hEiHAHKnRdGP2<gyf?LB51O6U157S^*-(QcOh8hhd?LAzTm=T~O@qr0rzwgo;&?7}Y_y7&VJv'
    '@>v6$AXucdVSRP?#?9@^=T2zTQ`zKnb!&38-&zv|Cuf;t&N_d<S7yyNm}ahqJ}L5z)}be-my2%XO{s>xW*Bt4N*6#u)@P5zjN-mk'
    'LLI4$C=t13jf(VfQj&PJ&OctW%GG&bDOlxl#YxH@uDOj!_V-|+YN5mNSEyQP>Fx=%xF#*s%g4n-jL#HiG#h55!MG!?4TNf`Vc@nV'
    '%GRu6&2oya4hGjcPo&+GVt2%Y5G66;r6aLHToz*y{HD=Y6P%~HrB(!ZR!sqXp8Ki*^d#uZ$tYaOYjsp~?ch<b&S)%+31{9aFBZ{8'
    'cT}obHs&`m;2{YG6a-R7)S;nlcGt`)j8=Im=`v=9)MIFs=rJ?X-3yCWS|K;8*#!#<Xv1fplBb8M8q9K%)`sk7UfVtT<L@87@nO2Q'
    'YYhEv>$(?pOd9o3YP~n~7170EyG`o>v1DoZ{gzC?>R@+w{r269H?Lg5x~3sPIQz02yVD?3{vfWGR~lH;Y+ky1d3XI*x=_0h?^YjM'
    'LVje4k!mbpbE&Q`&f)FZ4}CKj#=;57y8(TA>Z5oQ4I|b){@1rpUwQT68$W&c&d(pc_v6#={`*HCy!qruKYRH4k51qGe!4=!y1XGa'
    '4umspIOY^vq`-$ZJmC~aq`-l8#H)F|)Df@g^-@RdmPkvX|Jeu3I|f+9AMt(x91uriY6R~V@Eh+Hj2ME_d8dHic%Ohvjuf_jpLZ#f'
    '<z!!TTy&M6LhK<lN2mk{^Vos3>#{KVzYizJ0g<*~beR<KeS+^hVpS$^k~M^8fgH0BuW#QKuJV3EeluHE2{(P`;nN!Hu(pJ?C9ExB'
    'Z2^0t!#Wbyk+6=0g$rJ`7vwx`l+oq`2*Mq11_=cbeIVq4lll;mhHME*js+<)Ez2UYq0fGwzZ&92d^N=j=2uPnn!|?2V@P+81gL_#'
    '{0hDgZ1zQq|1-}7aZu7z5&(Q6cd|tCDl<#=6jp_Jvcx3b$<hk(on(<O+R`?Hws9r9BM31$XtSKRS+?8M2N)P4y}~I~{;VPWNTe@v'
    '$`XGr-?^jjPVHpe?+0dI2#-tMKNOD*h&hW;!JvtUq(aDy0I^dLTL*Dc5GMt3BuIvYL78aSF~O9QO<HMS^Lz5@s8@cgB*3=Z{7m!^'
    '<(5$#Wq3ao|C3gm1aN>x1Hj%&>g`Cib1)%s<1Qyh-eJ**g8_U>U7GoXnj8P^rI!xK+MtyI@%i-qS5Lq7&C|d9JM-ho8()`iC`QxR'
    'l)#4I0YF2WAFxkCplA7ghy>;N(HQ9hiBFn>vIzleoSjX2!VW+1nm%0d`PmT7a>l({hJUr3aj+t(X=k9&C6S$hQr#lwv@$D#GSv}6'
    '^3ldfykQr_=3G0IYpdK?D@&c47UlgEt*FWrFB##ApnFZ5^fmaY1hgN*QATU-2|wzDq9(jiH=Py_nnD{BPVudjvR+{yL=%3qSq8bp'
    'pT4b9fKRapN>hoCCZLTnxPs<Mmn_IOE<m$RK*fM6OHZ9)z@K&&Dx#qbI`Eer4=ExICPgZz8df_>Z{5itI8fcj-6?Bq_0^x&*t8*v'
    '+rxpxI~%RS8cQ071NA5AJ7>_!(3_hVH`v3kri!9*>Gl><<WROn<s6QJ%p2PqTJADyX2iu%-p=h^Evu?$5za*|Z;^3wo?7p{Fmzj='
    '%D6+pPhsC32xVF{D&mVD@653HR4mU6pNhJ}7YM`OPg}Jtra_1PW<8gd@KE{$S$Lh<tj}(<zxpe(Q6IhX&ktXGg@*a#xBvS1<=;R0'
    '-)|}h_&UVsfCTWq0k8V1k=whuy|=M%T;AP$b|c3V1SNjacFT=QgWfwqi1&88+IB1S9=YPxv#Tw<HpHvbT5i+pA+30jP+9br+epB2'
    'OF&dw?J^}`xyKba<(lJBLLZKcRii9|9}=>zZ(iQsyn1clxU{){JEg1alq=<SN|#fql(}X>m$%rqxn4ona=YQQb-I?_S~EkJv)nE>'
    'mo>V|OJ&z_Q@ZR4y0$lNY#W!?Z*8YEISsp9tLeO2achejuiBMHS>x4`TWM)Dfwiq=jizd=z2s$h)hfG{<&-8`5Kd5a>Gs8qUE}KR'
    '=4FjlWqZ+Xreu|=N8NHlR;vn160*wWcH3Rl$U?$OE7OH7l3$%w6}!n5D6$qo)g7zn4$J|jCsWZk;4K_US;rfh1B)K>k~ERffg6))'
    '6Yml4ls1yrMqbe-67ZZ?)QKcK=M{Y-3D5b2LZSl?#)G^T+u4<STpR`#^u28&6@hs<ZSQ<IXkoX{C79SVqh=6#y8S-DMkc2s@B#zh'
    'S2MEk3l2JY;~y~k<g&DAJg?a`*_<|Tu@l0ymK;{fgugU_PTQnghiSRK#XG|n<@58CX8Aps<p()pJ9Su&n2oQ<<xh<B9QcWEFcIJ2'
    'T#oEsV$i`otbq_jVy@FO)xw`*OMvnvSJy<K$hvqXDD}|Rh~=%mHchBxEItDeaC_BQmz#W;aR~&$tg0_C@oN3j@6{1aiIiO4LhL4o'
    'aQ0)F_h9aG*w%jXwQoLr>Gwj7sx6Iu$ceGLv3~jXDwO!n*7|LZM!if)9FDrPesgbQ)u^Pw9$V|%8+Q@QTd`>By}G-OaLgJ#{^QN-'
    'J9qJ7FI%<x9EZ5XBx01Zw{LMJ)a{{nv^S9|VF#Yq5)m<Q8;K_&fc)5j{LOQ0a(6EdLif<ars-zv^~_w$?+2CE-HxB*bv$gn*zd`b'
    'EzfQ3i;y`~)OGvbzQ`Gj<o8&7AIa}S-Z5ixL@aJ=*t`ed?3#*~Z3V~uYhJgNraV9F4QO^22*P21r$f>v-eSKSr}al2_nyoktCPcY'
    'VD3?`Uv*)IRncz0-}Lqd?r~q_5?p-U?|O<WaLmc*A-8vthMDACgNz0V(+Q5R3?fCJ>b;;5$#o8g7t3dkFIMT}E<wr{jy4uAN#NBm'
    '@|!Yn{5qaZ8PCKSH~NxiY5aLlnwDfk+E^}7%D%ET5e8jazLP{UH@qm8gF*xznKUjijA&dOx!s|M-pxTwH+C^pLceFyS8#JM@WM;P'
    'aC#GgW58a{>)@$+Y}G(N(C-n3{-LSqp?*GZ5d_I-7$f>DS4Pl0Q32VS7@N6kn;i8HjAqA&v6IHjAb#sAQ7*kA#CYYu<FzBRKa-*c'
    'fK#m}BcPs+fO;ypbt$-YDY$hhxb;cFtxpOrl$IuGi}eXft7jywt__`3Z0owH*QIJI(LdwK4_|-u=4+2$ek)}|1kAg^amF_ks+mNE'
    '78co^f-p~3p*Cqxepz0mH;3LTskQ|dSR$3{=8hEw)K@}YvJs0V!lwyDUsKwH*b9SXio0N}lyQ6@Tbw8mdm1vdhgAP0<xFxNUWZ42'
    '{qV_OzV+l+KRA8=7pulcfBv@l_)mYp0{^3T-!UJ*_xpTy^6Fyp;<hNy0p<y&D$l~g-nje5Ju*u$zl~O@NI`1fqH(fHD+!0>bG$0('
    'B0j-}B9jHD6*?VysFMEf9Mi)ReYcQ<X?GQop5Vq}o+J9x6|0P`O(VQ)1f)*0M0HU)KQrG>^J%av<sop-@}M+TRAAEP7B!X(i4yUO'
    'KG;j*u)kmhO%n~k&I>geA*N(sO%bt_w9T00X7e0wHY341TXL?37D^(7zk(Sl$lyw`%>mD7#5Up!kii!$vSpI`#qwAiC69jpz0-HT'
    'n+_4L=f^5|5^nS&yT0M(?)q&HbHNFs`-5%~px~!1M1}=MS0fkJ_;d%S<)wy+I(|DgrCEan$%%6+q$aJNQTKy<X274m@qZt__M4CX'
    '{1Sc6&FWiQh5U(GMO6-d`@~Qip@&%cH&+S#A84qff?0^rE}o1eJ~1&RjbV8~c_Dcv?k<Q4j`G+QNFwS)$|6-)S!SP_kfaL60^*R5'
    'm1M!AX)Wi^C5ER=Nen-0v;a%VUgWT49-&BpwX~wqLA9=cims#rxm@FCw)7r<`0nY8|0fkNsB1G78EKTQr3M&g$xJHDzr1qjV52?0'
    '5$<|%I5v}A1_A$+fX580-~o_M5SHy^Jh#wzW^0m|Gti`-b`kd=Cct^4CEO^=FW2YtoC(8PO_Tk)FiEVaJu-7h&E<tHoz6~~rp@LM'
    'c!8;b?a7jy5usspN@YcCG)SsMQZpW*aPnfMxO35vrhLrSWVEILWH=0AHPqRqmKYIr-IxZWlGb_gmUrZJO|T<Lx;|{TyPhfBX+T95'
    'Ozg*97*fQ{DB2<m!*W|K7&a~D3_%1(UU)8mG{qX-A)Hb=E92nsuuIFyVdR~~NzuLcGY!G=f-w(JGE;Zx^@yId`V3Qbj!8b6(ih2-'
    '*>vToX|i@^<IKu44L`Hyq^~B#3jBv<9Q09RY8VIoOc%vo%X}*63)VJzQ}!jHddA58?X|a!>o@l{FBvzsbEMq#gezBasGF$WIHEEj'
    '-RpaynY-tWu|$EdL!3hu{oz?8qO@wFuR~#HLl8H&cW&<U8B5Qig5uoe22nx6pb7cMAwXM`d?_N@AwV^r5jV~CD4h2M5`zzc%9r&p'
    '432LO^rU0`<(8}s>q%<(Wv}fHyUEyl%A>9sAQnO@zX{3EE4d6dX_zDZW$(;tv<0BBw9l+y%WKCvPB+ueGb><CS+dU~eHXq69a~F('
    'xqLqAvoL3PzN5cvL``=<10p-t>oail^kUbkL^2|tl7nGpv9@093X`8MW1o_bvWMkc9z&-+h^E(Ox!KJVVhvfJG4)JNb(oH4j;-M!'
    '8Ci_{K$9i7pYXAlyJOMfsyl3Xk;wv2R^g=Ipw3gi8vfIDHEHc~FRja?`6C$Ygu%c)6hY#t(pQtu3|@03Fk)iq@Q9_OBbI)N>5AiE'
    '*z7RQY)fY=fQvWx_o1Dr`_9)8N*$z!*9aa}c@ZCHVgh4Q#6D5;Pjx}4dM9Pg1Z$^~tv=S4ILeD1H`3nzktYsN8?!r4RMu~OGR^q+'
    'wrkGFw5-{2`-fg@KWSi*);4+ru^CGCcPrCMBqqv{7a0isYK^e4ajMBOl@rGz5kp03x@i&9b?_9<3mI&AX`$iJVmY;@>*+WmS~<Ez'
    'RVQ~lr}QC-AwoKXp<0?xyUeOJvA=mn=OworO!wlEANdWx>&Iik;#@H~s3t;SWJ#LATV6jM?HNlXtHwSb+xy|SzxVj3|Mu_~ug|&B'
    'xZgBV!#8kS7XvqJnO;}eN2FsiF$3_5xW}#^8*MLccFf#@JMb6SKN02fYRHh5i4wrjdOl(uAXo9EZ-_nD_OD}043KJNNM^*-E&s^i'
    'qxx%KXd>8dRc>k38$sCe!qsw}w*taaG;o`K|8Ui+c)c%Nc$!}O7xr)L7`3Mt_*tZ=mj%Lm0bVe!4~t+k!Vwqr#&f7t!hh*LZw)-K'
    'j4$1f*fowhy6ZMQbK&6W3tzsoa7aosmw%uTH>e1E)@TvSyAzbtko7&6x1JCDzDe+~h;ke_Vl-Xin_=GNc`wThF&#XZ?3HNPpw;&t'
    '(3_FgEoXNGM78I|od7#ZJ2&?Bu^Z*#z*B_F9&&O9D(#PHsw5D1Fd!Aqx_SYfm4m8k1T9(>{^Q<_Z7X6Aq~9JVJ4?z33bz<nx~lJ!'
    'L|7z3R<rGWz;^*C5yO0f2Pc<jD}6f0=A6%IQ{l<izw`LR-=y|$%U5dv&Dh2|Ds?DgHI@1lZOf@A&Twl*TTx-@M(A?+spU?2#&SpQ'
    '^w0J)33m+%P2wXd8mxe(qjxZRq?62YmgVtAb|>(fUJf_-Z3ZLWJ(w4+Y$~9gisZA21p^r<i+wLAU(}CDGDOL!3IG7w?9t*kn+ot7'
    'JR21n!q}F=Ru)P8fe31YJKeUbN!%2#dZa_M<6{_fCU)(_NFozZ-$se1w^6X)BGx6J#P7|O!w~cPZkNFIk@wu*r5n2&h8oLaB$Emd'
    'WUhfisAowv=A4|t8e>9PiT(L6T=?4$UNp8hZW-4$rJ~?9QSQNWa+N!^hMibPPOzz#&nf}IA7wb6J)|Z#Qq5K@^#}X}^J_*c)|}1a'
    'Vw9;lNV6B%wt#H|&}UL%b@&c~WyFBmYR8nLtkvG^BFQib$zm0naE5Q^8Dj;$SX3o;80K+oRa93JNqH53h6)ih#J2=UO4$7__Gab2'
    '6Cn_o3bK)BEw+_Wq<ocxPz^NR;K(A9GLT8c@Nv?>rAa}i=G)~mY#6m|kx$&%+D671#WMb(9)Xf=Eu2J&Dyr1#8LxOOE>emELJq)q'
    'Vq~z4Cp8xYb+{afq&8P)6K_&1v5)~OKA;g>LAy=E@s{6;J6U-4NJwBw6H&tLnJMlK9Ij0eYoM7LW}@J#RQbe-ZA@z5WC&N5F>EW4'
    'Kb2%x%2IX^WyhtlNAm5rPJjK!M=!ti=)2$0^zE@5t@|*4o>Kc)qE_WbEUD2Xq#)VkBE6wNWHcM^gNcpk%x0K0g!PRpz4MWtOG53^'
    'J+s7QrJAy&iF3*_DHS?|qp!jKl;xfg8{`GUu@;FJc*#p?$E>l20)?b;a+r{Ty(XITvD<rD2WKmH#=-j~ImyW>3&t8;)R=HAxTxXr'
    '7AZ9m+siLBEmhTI#G5TO`Bv64DiVd5vTAb5I>25N|E=8NB*k0t2@;4+!c(iZVMrSdMl)5BU6o>(Y^$?=g_2sNwkUOBIZl4IluT|9'
    'aao$!rx-#_w$L=IyeymKXbj;!Cp%#SGX=(hs=uc3q?SM-B-U}5DNEoF0$>DN_(Yx>8|mgL60~jEDRnCqZVGW>O>OG3%Ou%yo!;F|'
    '_kI;hCUKeDwFp&ZFJ~i8ISxpTh-YA_VUy88TL(CdZB?ay&d8m%+g-w`3Li8=7)z!6#71Kvzz=ZgLtvfEYOZK7GB5B=F!vdMG~j(*'
    'Uu*;rve@q{M_gJa@oMD>J2gg0j%_R4#QXL2ix-VYKl|;&@BP>?AN}%MkG}r?>2Ln~^w;m@HC)LunFxUp1y+Y9Q*1TrEAqe^NkL|a'
    'W0*<D*od~%hKpk=-2g_GQ%@2z1UK3J)eS_y5ggcLbr@3(#=l&5GeltF7z|~1Ku~!(EdbM$(@P@#L8dmgT!|?cfQCxiXbSWX%A<a^'
    '<m*Nw^xS)C;dCfJIK$g6HjqSnS&1ckrDbU^OT{NmSGJqFY!R5#n+7CzXXy${ZbX;3{A}$Zu4a>=F+yYFMLCOS*i5)cP;>apqP!c-'
    '2Lciko{hbNA(jMcHKVsxq?M$`fvKJt7dn_oOTZkV7f3SY-fAXvV1Up8v7yS7#MGb>eJh3wnT2?wS;?;Qj;rWK4P6iD#C|I8R!pK}'
    'E<17;gpro)vVvR_o0*l0hzy2JWx>NW9TreKb8lAM+cG0M!WYpIMt25Dq^<->UC~ZQ0ZNLN5E_E6r^Jz5y{SD}q>W{o*p@{~SEf`%'
    'f<}|lYMIUUv-Dber3!<yUK?20PM3C!>>W-?CVH_~f38LwSUhVEtfP@KA*``X87C<xGUX&m5jKhAWMl(l+$z_E{D2qqB7qCUK^VSC'
    'VE@dGys1579y$4$VWo8;%TK=Z(<g7dlPr0nLD^0(FB6?xGMqBPJ*ri8d0BcsCv5of<RVHfaV7^O&CzPnBM(l*$(2RAZV=~hn{JN}'
    'SV8#=MqIpxxzMpHP@i0J!KhdcZb@WVVZ=36VOtiiSu0Se=naI)ltdfh0ze$eOv;7+%1g}lBxXlqw#n>B@!3quY=lk*p)-MSf1;sF'
    'HI9<12=INaY2uyl8nkJSOPVD!#I1uX_0J<T_0fB8pT7Qm8J>4EkimtM*QOzOG<g2Z%p>1BJ|k1bebTbbW7XRqcDsD>8ZP~j@5;dn'
    'pM_~ookcoet8N9>?i~@Xrkzf*EK56_)MYQ|5isDAP_h34CvEC7h&*!#WACtwOLWy0NITX*+{q@%+Nn<xojLW}3f*I~M{~@G{>Joo'
    '!pDAPkPxC!eZ*eE%IC{ovynqR88spBEA90$$4q)wBk@GL=><o8XF_ss5pD>w21O%>iw<&#UjKN=?I2WZO@j3LZlmix>xHzs7DYr~'
    'y5b<rk(RL&_}J0I!O04rKDn}WV|~A<wip~J5>e_bq>ZzYHqJ(BJNZoS^pp=Sy=979H)Q1Uf(8<q&>vOXN9NEHcM~Nz#eIA!Xr&Dp'
    'zSv0X;29v|79x4WtGLy*sg47uur|Z;twSsz8AKuzmk~i^W@PboI8us4He`?47ePq&cQ@C!uWoJZvDWTceeL8|BVc=AQb?()B5te1'
    '#t`Hf2gIgDSwbZjIN#Xfh;`vV$8m_<7gyTeVyntx=5@PC@?yKO+$bZt<%aiEs^dCNm4UsnmvN&u-DU#R_A1Lw08!#)m1?^y?Zri;'
    '4q}ytV=wKtNJ{{#4ZGc_34+|D=61VLsV)hmgEWzk5aszU=ghdi?Dqo`&T=s@Ikt?uG!CWDS;%#GVwTwQO{Y3H>q-&9>**pc1&ogM'
    ')1qo^jRozoGb=}32)eVW)z%1jbZd+4%)UBDPd$?^kD_C?+RKSglDF$bJJB|IOdBm5naOkwy=&?LSU>`&WVXlyVP`yk@egUVuy@E2'
    's0StJ@8}pOzr~X?b<F#q3+cPVrY99k)-Qths0sj>ducLfranWKQne;SU1?pGId2R7h`zw$1^2<iA!Y%X%D_6AJ$>_z!4h0)JkP6Z'
    'rTM1Ix=st9_N+Lf<uu4lj`tPbh3X<sP;OZmC(Iq(_k{~R)mEV@zqp(*Taa2}3e6Ih`K8Pfr4(_`E$6kf-a0AHvPMb;jud#8@W7N{'
    'Y@SaFBT3qV!rY!^fdHdeII4&QNr6J5`u+W1J^9st&P|d=)(aMH5LCV2YH7cvS0_+r9?U2)mAtl1SVM~-gjbibj3P1SH6@WseZ<}q'
    'hd&XaoO0fB*w-VXZzsD>Z!aN1TN%aDB*)4L!?=}S|DkN|zx><d|Ai}RU;FU%#h3GE?0ThlZe|JKu4gXH8@{lZCF?=5vq-(q$>mCo'
    '-;2ri6KKp*CHa5)+rLb;Q^eBRLc~fI2mF%W0b*2<c84@u>$n+J0N6_3m8IMy6bd&QGksFdm$X7wnYo`7tBHfm6MZzh)Kbb0crh!&'
    'n>njgB86DtyzwrzPb_jK_^`z6URst;heXnFv0fr*CE`jVSZE>BI$iUMPA?Cfn&7ZxC$)jusmW;3kY2uN0kvn#XBD4zG9s591)gyI'
    '3<>?{-B+Ic^xIk88jbj{9*6DTnW0&uk#wMvi15HzRP~B&Q1yX&Y3dfuE~hF)lrO`jP~sk>&!q$f(1M$GRh$OPZl<Q{MdtCEOmEd}'
    'YMCL-rKK#j;zQS4Q#^X|;RmPh{HN4iQ>rwJ6O@-1<;OWVPrvi?M}PX^gh)Po`IYl~Vn#186K(!nQX>~D;nb)8j2y%jc*Cfa9J{Ih'
    'C<-)Lv0conjD$@2@L<9Qy5u(FVZ=Z1kY!R}jTj*uu@iH66O9Y3=B(MfX|-_OkA)kQ<h&_N&)Zud&fz@y1j5PslbxB)!`ZHqxY+4h'
    ')iK`K-jK?sBDKy8gt~A+Cp0ZL^$~yE*h%e-4qvlGloViPD?<Y^tgieM|EBvH=Yz&mjHoOp18zB?`?8#SS2Tp_KyXrNl$DTOs;)E<'
    'Ka-(Xpja~tyUvuUN|>TaaviDK68$i%-!k?>)`vZN-mJ`;H+f_VR`Y<s45?n305t~6tjT!Hs!>2|0eO)|b`(t5F=vd09UKfhYbXde'
    'e`2rmK8Nsu6$BsDKvCBjt!06=DF<{f3QI=NJ&4(|6_F|R8S^`{*`AtYmuj=hCn~O7Q8T)-^Cu)lj36=Jl;xAg$4X)crdlLRSWS&G'
    'R$ocaU<wfC>2lVjv8Pn@8}FQc<Bd-<jq#Ybg=LA6z^QGvo@*0Rmarbnsp;%+!SagWs^Z~gWl2?LmS+x4RaUL(M6G11v3Ya0yqsDW'
    'Qyp!bKlwRwuD1CWLv5m!c=ZsaiMe!o&f^<xxRYQKC7o4~Y9bZJ%VH*3*3q3YWNrmvx0N|}dYt}D(lNpxihNtUOzC*yWWUS5v~Wzq'
    '*r|V7Up0OmXw5Je9p0T5E?dO$@J3QWEg`3m8Id8pII)E_wd{5B(!rZv8ns~9%bKs7{ZV4$sgQijP!<8fzuTd_-ePMc!iDr5c8th8'
    'dooWeKgK@Sfj0tpQ97D&KhPoH1SK5FMdd**DvvQQxSzGeFD}8EtN-W{2JABLAU$jGuNuLj%YGW*O)rAG!w~pInWKSl2@BtEvSoJq'
    '`fpF)`vX}*hWYTDub%$-cTc|d#*+_zoKJhl4Krjy_?&VX;pftb01J)=;@5`=TCj-{YDg%H=M|Od$V?k|zBP|U(aK~|+n$0KcdyAw'
    'JP2>|#YNPa&0}r~e3I0z0S-5dAwulv$lna;dTz*`KNC8PN^?upv#mYjZbn;q1G${ZzaX%6V^_L$?_S*8H@=GO%NslU*R)hstmQ}W'
    'otg>A{>I+EbOfeZ7q>RHFHfajy1BJ=_saUEjkJT_eCyF$@6$8f;Co-WE$<J2%aq=%q2|gu%W(`i;bG4GJvTRfI=`|r!v$Pcs}Diw'
    'E(eP(r$gK-+qGF9SX{LXd7t5A#a-Sk2Q%{cif;}roRKMR{!VW#nE}E#0W)p09KS_lcfwul2=DW-4|_-M8lh3Ja#>X8sma*aawZB^'
    'gl`+Sb2CA>6Q@3%&v$q$5uF9VcV06<<erg#QRX)iDLuz0U6~N&nKCe^De%L~yeVoswR)mfp8V)%bK3sI)Np`2i~FSULgmGaF42c)'
    'inN4H_f0<0onPlk_2D^UeR#%xNg~&0Y+B%F93<$`%$~(H)lk~A^7!^@?livXXa)q|Y@L{8vmkIMa4I;nWDgfJ3lP33X<FXp_1H3;'
    '_3s@m{BsQ~AfH6;7Bl*Ab{|Q#_~_-gKKkH~lLDrxPnIuiDoN>*`%C{roh5$J!r0QZTy$@|u5L||gFER9WzJ9SVBN!Z4i%ItWQF65'
    '9GPa%NOSbGsV)|B#6M_}^szwgSYjc*sAbq^WjL9P*@Bc6wds8ED-~ym>kMI$dgOP%Gt4Ki|HtFk-h2Gv+ovD=NB-P!96kar4dosd'
    'dp(P{2;iQ_Pl{q?2cId27V*+)=k~6G>RHEZZdN#9Myle6zGKa?HOv<$FP0V#zbD3PP1|bu({CRA>q`%R^1E{)ls<0xq_>dQ7R#Uv'
    'abj}SI=NVItg61%Kz3u5S2K7zNY)>gb7#g{LBHN)U^S&95bB7mYSodmDy{MYN>#d&`1X09QW*3JgU<CGmJ(NImD`!w0gwx*W^o1<'
    '$#M}Vn&o%EUav-0V5Y(eGd?xxbk=<fNv}Tq+IOG)<y&(`7FYJXEF%071H?ye(k;vBC_p9mPyYEk4}b9ORf7z218+Y$eg79Q(ihZ)'
    'C=-fLvnCt3;OYvk?U25=d+F}_*3Pwcp1p2tZ`{4UxqWl*ZjvrFt~ZD~*WKuzb_aqkY1l*+PCH&Wrw%0qyOd<Gi!HYU9BVmEt0k95'
    '%f$m6fxIx}K`EfHfal`!$4Nf673skgUR++FC0+jPh&a6^U1)`_HO9wD(iGlK=LYfz!rKZ4X$iR^&8PFQy7yW-bFp0IAkzF)q@Wnq'
    ';&z!V4Fk|H01Z57HAj;SbX%Z@o;%7=H?VNM40|h3Vdayi@O3l;%i~~%GT+6=lxBKe90i-bLis#mmOgs-gVVpf{pfqYCAx5_{)?|X'
    '{;!{({>yhrs*`A=Sx1!-e!-DAi}367Z$lg6+8%zU#X-v*#PWW+TjJ}Qya8{huCdc^8N;ta=}wN;Ak-t>THcZ0^mhD_*WHDo$=BQ$'
    'xk7@(tv7los=cU=u!-X`e2|NeiXbYCFc$>LIB}GTVO^O~?izbkCJQP#KW0^O3-omO@fw8c)`W`&u9!MAAmgUN&yLCiol|Fn1y6EC'
    '$s9fIs*T@vGpQd0!$R+cp%=yLeZR*x_!Z7(puGAqffoM=Cl#TgjXuqb!$b0>G=yaZ$8t+A#ubo=spK*oP$|<zm}h!MT!;WZVd=n='
    'EF+c6WmX>iLs(J}lA~n6CDShOEUf>i18&7t@>et-{p|gZ{`w<h$2Xq5@r{Q+{29+dsbHmB4j|zIVng`|9%S)?xN1rMQh8qee!1S)'
    'I)D=4lGGSVATxJitD0~h6zRyME_tn!{2BD=y5w0+1)%DhXD(0Hg}?MDo>ccTUvmc{g9lQEubd)#Pgo`CV4FB;HRHfn8s*B64L8J3'
    'f+xR>t^|3)d$<Bos?|il3m2k1E%pyN?U={M+;d^F&@4cha1r7a8t5%k9y+_Svu7Cp?@tCF))WERFq}=n#)4KK+>u*1Zt>wuV`ozw'
    'sZ3kM;ps_x0-O)$iy1`NI;<Iu;HgMq?RX~+rGA1lr71%(#FNwf?Esfi61r@P6?$%KT%XH^9+!oL%)CEITsxZFxVTcEJEnDZaBSVZ'
    'izBccV|J+SFEzzvr|!avJ-%&%uf|x-+!%t3OCh8v$cIUfgh-1E9FMpduu?bbIMWVHAh?4v^&)|@#r2yH>T~BSFA;G1{{dw{d-V'
))
AUDIO_JS = _unpack((
    'c-pO6?T_5V8UKEN#pFX-JLlWj-uK%a)g^&YDTt7y?T6E;@_J`?-SgUu?Y+x2L?Q)Bqy!Stf<zG@S_!4lii)bOM4|jM*~{I3(dU^r'
    'k9XI1xlmAip7Ar!+dMD7nY+p~r6kRgz|Sh(m2>CFlSlVv-#(b#|8Vy3?!n!M<obS;jrP1<N)F$=fAG=QN1y%U;L&f1@k`nxo6~*}'
    'Tjc2Df8p$xf3V2mcOM+R^8lvq`~}vNYhF6((InX?R|9j!kE1jr<Degq4HA)!=SjV8le6SyFB?@S@t)yY#E8fmX?9F<jySH_T|t%F'
    'WcK$5PriO*_Wu3ZcV8U6@y+4q_ldCyoT4}}*9qAilNZTFa+$o&UoVpv#zNZFYp+}eX<I9V+#*RFXX~U^vq%<4G+ifKjh024HvFq^'
    'liQXeaXT6bkaIF5(fKqrqQ+7_HK$0@0KQFkp3nbFpHg8tpSDH<-sWVC&vsXM?8*z9mxRZ*+Ky$z|LjMrgAcIT)&}sXTlO}pvDIoZ'
    'V)lc7as{y%*jBTnh&$FCp8_#Xw-x7hZC;JKu0|anjv{tADK1w_NWQ+wc<DOBgMVu27Ph3)c0mnzw43}V<CyD#GHV*^+z>{JL(*<@'
    'hB=RI&GnntuA=9G4)}sUYV65m5C^DM{Lo8N^71qdd~yqfuw}{A&*H=|*$g4sC`hY*b`x`K8irjy5z<{6!jvt><7r0wFdleeO1t^O'
    'oxtBoQHgCqm}YdMt&8Z*?1nb(O~x>C>aG}P!I&meG_bu5|I*A$GNoTIAcoWt<_cqw=4F&@Y;2H9I!z}u>eGJ3R5n!;noh^mFuNq7'
    '*))l|On`6%*}Mpn_kyS&?^RiCx)?_pC`?{|T~6=O-cFF|AG=DcGn*Gp$yej*15@3pbPog>w@3)8M*jXwK?IpqfhSEoKMQtgh1@oE'
    '218h7?4p}YEPA)ZG*m$1SN((npUYklp;b|J2yfM0FPwrK$gZ@LprzV2jXl^G^z+crw)3aNChNqmwi^ZcemtINvM%jM-Z=2ni!crT'
    'OfhyO`FK*zMld;w!@kmD&1rV|x5UeWSj{)Yte0h;zoVw@s%_Wg0vb{;rP?>Ap_$=DUbvq!L!@?_VhX)cps5Z9+4bNz$i;0m7kp6#'
    'TO;ac2Ff*scsW;Kw7^)ctoCV|1rZt<370_o8MAcjO;fV=JPZbdkdi?VqW^J%N!PUD1i3*Mg4d>A|3$Vy8O5op+5QAcD`C7hfy}NH'
    'zYY@m+7v@fxzB0awyl|tN?{B*k}pgYjpnT8#1<)-0j9<^9o)Pi7~9pBT+3&VSqrY3{q5oG{?`ZpymRp0`#Haf*S|2YD4#2G1Lbu!'
    'df<^4PjVz9D)S@%_^NVWeUAHrR(wHGDNd(ToTRvyOit7rY0A`Q-xfE&<`(vzQI)8HTk-Lyhj+dq#?eP_9sTFi+1p>u?*0x?+LOP2'
    'VdgygH1ziM(tzXK9qcoI-hjHUG-=uZ&s6z83t8Q2=mlrc6Twq!n-=MZ$2g-OF7X0PE}HK)3+AWL8-$dG3Q?FVx`gRoG)I2#hg`fI'
    '4|*^j^p>t?Vl~<&?*8aY@UG^Akn;MTdgDn*uYu_niF&#xAQ!<0(A|O5Do~=+u+#LaLz-P2c_1{r<Yk^=3xR_;Ax20u67W_Wkn_j|'
    'URGC4(%%ZUVV=S2#DlgshUR;gxPYu3&4W=Kq?C!#Cq;h;EvHFBqYO8mtYYETsAQK<Y4$Vhd$31_!J3=+?C%(0gv<L7!vHjU8GDp5'
    '#-3k*AmeV10YpJ56n54TVf_s+0e5UNjf}C@?5rFgXi8hyh%hvS_$!Ejj8KV}h$!sl3SxCMp!Uzf60@W%&np#2pjEwrda+7frWm8M'
    't8RlCV7G;m5Jq;j>X3tb??NFxeCzJv=bu>Q$p>E@ee$Qne}DG)`v(N!89Dm!O`z^U5EVexnOt1~8f-l&qj*mPGP**XYHt)k-!gI('
    '2p)=t*@!&%oCXcI;M8%R@mfPTqfw`$V30{9fw2i#HAD2!>GF8xYV44Bpe-|*>O1881~N6}q8-jg*uf&1-kca~2A7Of7}6~jUu-vR'
    'XNf~p+h6JxPx?fXS<vYRa`IO_gpP)M=iu+>0QK6NNdlG9lc2;Dc6*qy7xpuXe!UcrA#_>d0#Ddv^valL?6M37BH?o!uR^~v896h5'
    '?A<iR7Jv78DRRU#hh1>nQo1m3%nr|O=^CDm!Y_-EmS^7?e;M@cPm_gme@?bhJz#j*IKQlHG*rf={s;<yI#sN$T3XF93kM7^9%S>h'
    'VA;u*;wo5Ev;|u@JEZ)CIB<6Bd5Lt{AdCUqvTxv!rU?{q{`E)j9j^tpfOOj;SEMgk2<4}NE97~G*tsk|mja7AJD%8D>>HWzza&C}'
    'Iz|qEbzDK5MqWY}s3l8DHG;g(z|3Sy6(xmJnj&|(2AG&k$+?B>NQc$0Q4qvPYqGTEe4LWiHLRVvJxm-rcisbj;-w=rN+WiP?m>1<'
    'Q=ZkhIy$Qw@=lq*=Ul}Vfj|PrYwRnc4R$lcSwYQw{QY~-de_O(oga=qyvIxA<L}?K$n4G^XYYJV(x6ZM5o98nOyMAO@YZJw?mwg1'
    'g9r}=<2{w(LkErHj4Plv3aYo`V(m6fYcV^RiX9e-7D<=v0k?MEk4xpE&5%}Z9Yo5xb@^sm%okD;j_PvHZ%bhE<RM<p5o7lDqbHB<'
    'nRDUIgH(l79_>80*j*9c27pBN4&@&+NDLf(;OYbD604y4wlrQMR%IY3+q`yl3&pp$IlXBSp%-|VHOFSb9;LWz7LL()XT{QaE8XUC'
    '7@0Duy}l9}m28(=b%o%Xic&4|O?6~JPSQqe0S4DqH=@z5F$7Qt<eo())Y}0>XAurr@qBEn!ZH*`e&36H8eYdbHw|h37l?XOmR6Di'
    '&<2|oV1u*4a@Z{}3WJDx$u$6zH)5ThYk{HcX-uK3f-zARc;Vs_&{wR0e|=?LocacWb|@CiM5xs8fTJ@$vuVT*`o$t07oZ2jzptcz'
    '5QZMRy6Tcx9s}?P4i^sq1Dxgp)Epmj2gEtF2VEFXe)A;XV+cPq1e)5a1c#z!#?m%fu*7vuS<|$bMg9^~EOy;9cdsM#D<DVR(GK4E'
    'ay4_BW4EU6@|}SKP?G^r5+<Dn#O5yNKYWT^$G~zVcR0b#dw0nAEFOi*{0&vfoWEhLPNuwR$TFph^g4k&BdTsa{^7s8qR;;Pdnokt'
    'mkKB4&I0LzciaZ|%mQUu9x2zjDk0cO>ZO47PnHZKJ76mzlH!nO$8ph=E*uQ6$J4~87*B)J<8yhe;g%p5DTHYVsI!=5gJoF;Gx+6I'
    '?ar=!T!1nAo*}ltQA$~L2FD|KNuZ$%v0Z5am&$;%77n}oRv=xH_4&3bj8RDT++SixZR`$}9`I(@6L73`@n{DUSYj<)_0H8fd9_=X'
    'p0yv5oeBueRavail`ILoXc$t^*y-4;QggU4JWZi-99u~%Nqi9;g%5ZYqZ}=uWjw))4(aSgN8@*XFy`mtI;3W06bwhg@2v*<-B4ss'
    'i_t*=<om#6NjSPpfK#m(IW}y*lddaPOAs~?i7b)TiS3{)5g7%817ZVgyUt>V@47nLF=^~BVBrc>+o{q*SH5H}-a598U{;`SbX>>Q'
    '3gG<e<3poqt5gO?4hBfB2#dkg+sgo{jw%{f5Y3mzp+*XoEx}+NK=pSQi7irJ9%@Wy6>9=yg0$V@ejSsVOE#&-lEvY>1aHlgO=ERp'
    'Npr-D+CrM9<(j0$-~Zs@N9V_jUU{NPv@64RFb%^W;RT18-mtV<ef-w4ZCdLT_qB|!W9El#uISQWIGYCpTV|I;0qY2-cX0DG{uM_6'
    'f&bAfrz#1@^>T5syW}=}P@c`KAZBKfrWCle?Lxlt7Wp(Qo7%z?z@|ErNQyF^SnC?Hv(%62kBSVnUc;1lD&{)Q(BK-;?;<017m1sx'
    '+Qodxs&k`Oj%qy2+ht*1zNW2?m%|dwqrp%WbpVgo;6H+YWb?sY_KxUfaMRccAUL1?W>22#=kNEIwy%Yb&VK)=<tz&4zpDTBbUdk`'
    '3x_9w?9&6Bwz@xA260rGaGMI?v`-0eTFo5bG}Qj63%A_L(2MA?RwA}~CM)fhDqW=zuHi}x?bazR?AXdeyLp0z{mN40glTByMTsFN'
    '*74*oUu1NYGam;bAo%zMAG*)#!~C*yNqDr|^Z0iOkyCT?NMM&~<)m8BxRyxo<BabIw9K*1f?s)&X0wY~S6+5&&zfK-<X2wQ>MH(D'
    'n_zY2s+P>J+bg$M#2@7FKW5tCf7H}n`5$k9MGy'
))

def load_scores():
    try:
        with open(SCORES, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (OSError, ValueError):
        return []

def save_score(name, score):
    with LOCK:
        rows = load_scores()
        rows.append({"name": name, "score": score, "ts": int(time.time())})
        rows.sort(key=lambda r: r["score"], reverse=True)
        rows = rows[:10]
        tmp = SCORES + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(rows, f, ensure_ascii=False)
        os.replace(tmp, SCORES)
        return rows

class Handler(BaseHTTPRequestHandler):
    def _send(self, body, content_type, code=200):
        if isinstance(body, str):
            body = body.encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(body)

    def _json(self, obj, code=200):
        self._send(json.dumps(obj, ensure_ascii=False), "application/json; charset=utf-8", code)

    def do_GET(self):
        path = self.path.split("?", 1)[0]
        if path == "/" or path == "/index.html":
            return self._send(HTML, "text/html; charset=utf-8")
        if path == "/game.js":
            return self._send(GAME_JS, "application/javascript; charset=utf-8")
        if path == "/audio.js":
            return self._send(AUDIO_JS, "application/javascript; charset=utf-8")
        if path == "/api/scores":
            return self._json(load_scores()[:5])
        return self._json({"error": "not found"}, 404)

    def do_POST(self):
        if self.path != "/api/scores":
            return self._json({"error": "not found"}, 404)
        try:
            n = min(max(int(self.headers.get("Content-Length", 0)), 0), 1024)
            d = json.loads(self.rfile.read(n) or b"{}")
            name = "".join(c for c in str(d.get("name", "PLAYER")) if c.isprintable())[:10].strip() or "PLAYER"
            score = max(0, min(int(d.get("score", 0)), 999999))
        except (ValueError, TypeError, json.JSONDecodeError):
            return self._json({"error": "bad request"}, 400)
        return self._json(save_score(name, score)[:5])

    def log_message(self, fmt, *args):
        pass

def lan_ip():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("10.255.255.255", 1))
        return s.getsockname()[0]
    except OSError:
        return "127.0.0.1"
    finally:
        s.close()

def launch_browser(url, kiosk):
    exe = next((shutil.which(b) for b in ("chromium-browser", "chromium", "google-chrome")
                if shutil.which(b)), None)
    if not exe:
        print("搵唔到 Chromium，請自行開瀏覽器：", url)
        return
    flags = [
        "--autoplay-policy=no-user-gesture-required",
        "--ignore-gpu-blocklist",
        "--enable-gpu-rasterization",
        "--enable-zero-copy",
        "--disable-infobars",
        "--noerrdialogs",
        "--disable-session-crashed-bubble",
    ]
    if kiosk:
        flags.append("--kiosk")
    subprocess.Popen([exe, *flags, url],
                     stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def main():
    ap = argparse.ArgumentParser(description="DJ dino RUN 3D")
    ap.add_argument("--host", default="0.0.0.0")
    ap.add_argument("--port", type=int, default=8510)
    ap.add_argument("--kiosk", action="store_true",
                    help="使用 Chromium 全螢幕開啟（Raspberry Pi）")
    ap.add_argument("--open", action="store_true", help="自動開啟瀏覽器")
    args = ap.parse_args()

    server = ThreadingHTTPServer((args.host, args.port), Handler)
    print(
        f"\n  DJ dino RUN 3D 已啟動"
        f"\n  本機： http://localhost:{args.port}"
        f"\n  區網： http://{lan_ip()}:{args.port}"
        f"\n  Ctrl+C 停止\n"
    )
    if args.kiosk or args.open:
        threading.Timer(
            0.8, launch_browser,
            (f"http://localhost:{args.port}/", args.kiosk)
        ).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nbye")
    finally:
        server.server_close()

if __name__ == "__main__":
    sys.exit(main())
