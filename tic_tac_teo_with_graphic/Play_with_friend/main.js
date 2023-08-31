let lbl=document.getElementById('lbl');
let cases=document.getElementsByClassName("case");
lbl.innerText="C'est le rôle de X";
let gameOverConditions=[[0,1,2],[3,4,5],[6,7,8],
                        [0,3,6],[1,4,7],[2,5,8],
                        [0,4,8],[2,4,6]];
let isGO=false,playWithRobot=false;

function robot(){
  let possibleChoices=[];
  for(let i=0; i<cases.length; i++)
  {
    if (cases[i].innerHTML=='&nbsp;') possibleChoices.push(i);
  }
  if(possibleChoices.length && !isGO)
  {
    let index = Math.floor(Math.random() * possibleChoices.length);
    let role=lbl.innerText;
    role=role[role.length-1]
    cases[possibleChoices[index]].innerText=role;
    lbl.innerText="C'est le rôle de "+(role==='X'?'O':'X');
  }
}

function click(){
  if(this.innerHTML=='&nbsp;' && !isGO)
  {
    let role=lbl.innerText;
    role=role[role.length-1]
    this.innerText=role;
    lbl.innerText="C'est le rôle de "+(role==='X'?'O':'X');
    isGameOver();
    //robot();
    //isGameOver();
  }
}

function isGameOver(){
  let casesCentent=[],count=0, pointerChange=()=>{
    for(let i=0; i<cases.length; i++) cases[i].style.cursor="auto";
  };

  for(let i=0; i<cases.length; i++)
  {
    let c=cases[i].innerHTML;
    casesCentent.push(c);
    if(c!='&nbsp;') count++;
  }

  let verification=(i,j,k)=> [(casesCentent[i]==casesCentent[j] && casesCentent[j]==casesCentent[k] && casesCentent[k]!='&nbsp;'),casesCentent[i]];

  for(let i=0; i<gameOverConditions.length; i++)
  {
    let [test,vaican]=verification(...gameOverConditions[i]);

    if(test)
    {
      lbl.innerText=vaican+" a gagné!  clickez ici pour rejouer...";
      lbl.style.cursor="pointer";
      isGO=true;
      pointerChange();

      for(let j=0; j<gameOverConditions[i].length; j++)
      {
        cases[gameOverConditions[i][j]].style.color="#eef4ed";
      }

      break;
    }
  }

  if(count===9 && !isGO)
  {
    lbl.innerText="C'est un matche nul! clickez ici pour rejouer...";
    lbl.style.cursor="pointer";
    isGO=true;
    pointerChange();
    return;
  }
}

lbl.onclick=()=>{
  if(isGO) location.reload();
}

for(let i=0; i<cases.length; i++)
{
  cases[i].onclick=click;
}
