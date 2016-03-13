
var Friends = React.createClass({
  render: function(){
    return (
      <div>
        {
          data.map(function(item){
            return <Chip name={item.name} pic={item.pic}/>
          })
        }
      </div>
    )
  }
});

var Chip = React.createClass({
  render: function(){
    return (
      <div className="chip">
        <img src={this.props.pic}/>
        <span>{this.props.name}</span>
      </div>
    )
  }
});

ReactDOM.render(
  <Friends />,
  document.getElementById('friends')
)
