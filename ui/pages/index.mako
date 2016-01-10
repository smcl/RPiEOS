<div class="jumbotron">
  <p>
    Taking a picture every <input id="seconds" name="seconds" type="text" value="${app.picThread.seconds}" size="5" disabled/> seconds
  </p>

  <p>
    <a href="javascript:editClicked()" id="editButton" class="btn btn-default">edit</a>
    <a href="javascript:cancelClicked()"id="cancelEditButton" class="btn btn-default" style="display:none">cancel</a>
    <a href="javascript:saveClicked()" id="saveEditButton" class="btn btn-primary" style="display:none">save</a>
    <a href="/snap" class="btn btn-success">take pic now</a>
  </p>

  <p>
    Total pics taken: <strong> ${app.picThread.counter} </strong>
  </p>

</div>
